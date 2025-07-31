#!/usr/bin/env python3

from re import search

class Version:
    def __init__(self, version: str):
        self.major, self.minor = version.split(".")

    def merge_version(self, version):
        if version.minor > self.minor:
            self.minor = version.minor

    def format(self):
        version_str = '    <version>'
        if int(self.minor) > 0:
            version_str += f"{self.major}.0-{self.minor}"
        else:
            version_str += f"{self.major}.{self.minor}"
        version_str += '</version>\n'

        return version_str

class Interface:
    def __init__(self, name: str, instance: str):
        self.name = name
        self.instances = [instance]

    def merge_interface(self, interface):
        for instance in interface.instances:
            if not instance in self.instances:
                self.instances += [instance]

    def format(self):
        interface_str = '    <interface>\n'
        interface_str += f'        <name>{self.name}</name>\n'
        for instance in self.instances:
            interface_str += f'        <instance>{instance}</instance>\n'
        interface_str += '    </interface>\n'

        return interface_str

class Entry:
    def __init__(self, fqname: str):
        self.type = "HIDL" if "@" in fqname else "AIDL"

        if self.type == "HIDL":
            if "::" not in fqname:
                raise ValueError(f"Invalid HIDL format: {fqname}")
            self.name, version = fqname.split("::")[0].split("@")
            interface_part = fqname.split("::")[1]
            if "/" in interface_part:
                interface_name, interface_instance = interface_part.split("/", 1)
            else:
                interface_name = interface_part
                interface_instance = "default"
        else:
            if "." not in fqname:
                raise ValueError(f"Invalid AIDL format: {fqname}")
            self.name, interface_str = fqname.rsplit(".", 1)
            if "/" in interface_str:
                interface_name, interface_instance = interface_str.split("/")
            else:
                interface_name = interface_str
                interface_instance = "default"

        if self.type == "HIDL":
            version = Version(version)
            self.versions = {version.major: version}
        else:
            self.versions = {}

        interface = Interface(interface_name, interface_instance)
        self.interfaces = {interface.name: interface}

    def merge_entry(self, entry):
        if entry.name != self.name:
            raise AssertionError("Different entry name")

        if entry.type != self.type:
            raise AssertionError("Different HAL type")

        for version_major, version in entry.versions.items():
            if version_major in self.versions:
                self.versions[version_major].merge_version(version)
            else:
                self.versions[version_major] = version

        for interface_name, interface in entry.interfaces.items():
            if interface_name in self.interfaces:
                self.interfaces[interface_name].merge_interface(interface)
            else:
                self.interfaces[interface_name] = interface

        pass

    def format(self):
        entry_str = f'<hal format="{self.type.lower()}" optional="true">\n'
        entry_str += f'    <name>{self.name}</name>\n'

        for version in self.versions.values():
            entry_str += version.format()

        for interface in self.interfaces.values():
            entry_str += interface.format()

        entry_str += '</hal>\n'

        return entry_str

def main():
    entries = {}
    for fqname in open("fqnames.txt").readlines():
        fqname = fqname.strip()

        if fqname == "" or fqname[0] == '#':
            continue

        if fqname.endswith(('.xml', '.txt', '.zip', '.pkg')):
            print(f"Warning: Skipping file name (not a FQN): {fqname}")
            continue
            
        if not ("::" in fqname or fqname.count(".") >= 2):
            print(f"Warning: Skipping line that doesn't look like a FQN: {fqname}")
            continue

        versioned_aidl_match = search(r" \(@[0-9]+\)$", fqname)
        if versioned_aidl_match:
            fqname = fqname.removesuffix(versioned_aidl_match.group(0))

        try:
            entry = Entry(fqname)
            if entry.name in entries:
                entries[entry.name].merge_entry(entry)
            else:
                entries[entry.name] = entry
        except (ValueError, IndexError) as e:
            print(f"Warning: Skipping invalid FQN '{fqname}': {e}")
            continue

    fcms = [entry.format() for entry in entries.values()]

    print("".join(fcms))

    return

main()
