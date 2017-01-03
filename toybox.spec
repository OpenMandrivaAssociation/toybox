%define debug_package %{nil}

Name: toybox
Version: 0.7.2
Release: 1
Source0: http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
Summary: A number of standard command line tools
URL: http://landley.net/toybox/
License: BSD
Group: System/Base

%description
A number of standard command line tools.

Toybox comes with smaller, but almost fully functional, replacements of
the command line tools in coreutils and more.

%prep
%setup -q
%setup_compile_flags
make defconfig HOSTCC="%{__cc}"

# adjust some settings
sed -i \
	-e 's,# CONFIG_EXPR is not set,CONFIG_EXPR=y,' \
	-e 's,# CONFIG_TR is not set,CONFIG_TR=y,' \
	-e 's,CONFIG_TOYBOX_UID_SYS=.*,CONFIG_TOYBOX_UID_SYS=0,' \
	-e 's,CONFIG_TOYBOX_UID_USR=.*,CONFIG_TOYBOX_UID_USR=1000,' \
	.config

%build
%make

%install
PREFIX="%{buildroot}" scripts/install.sh --symlink --force --long

%files
/bin/*
/sbin/*
%{_bindir}/*
%{_sbindir}/*
