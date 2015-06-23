%define debug_package %{nil}

Name: toybox
Version: 0.5.2
Release: 2
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
make defconfig HOSTCC="cc -std=gnu89"
# Enable some more toys
sed -i \
	-e 's,# CONFIG_EXPR is not set,CONFIG_EXPR=y,' \
	-e 's,# CONFIG_TR is not set,CONFIG_TR=y,' \
	.config

%build
%make \
%if %cross_compiling
	CROSS_COMPILE=%{_target_platform}- \
	CC=gcc
%endif

%install
PREFIX="%{buildroot}" scripts/install.sh --symlink --force --long

%files
/bin/*
/sbin/*
%{_bindir}/*
%{_sbindir}/*
