Summary: VRRPIPTracking
Name: VRRPIPTracking
Version: 0.2.2
Release: 1
License: Arista Networks
Group: EOS/Extension
Source0: %{name}-%{version}-%{release}.tar
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}.tar
BuildArch: noarch

%description
This EOS SDK script will ICMP monitor an IPv4 remote adress and update VRRP Priority levels.

%prep
%setup -q -n source

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp VRRPIPTracking $RPM_BUILD_ROOT/usr/bin/

%files
%defattr(-,root,root,-)
/usr/bin/VRRPIPTracking
%attr(0755,root,root) /usr/bin/VRRPIPTracking
