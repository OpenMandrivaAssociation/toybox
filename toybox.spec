%define debug_package %{nil}

Name: toybox
Version: 0.7.2
Release: 2
Source0: http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
Summary: A number of standard command line tools
URL: http://landley.net/toybox/
License: BSD
Group: System/Base
Conflicts: coreutils

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

# (tpg) disable these as they are in until-linux, procps-ng, grep, findutils  etc.
for i in ACPI BLKID BLOCKDEV BUNZIP2 BZCAT CAL CHATTR CKSUM CLEAR CMP \
    COUNT CPIO DMESG DOS2UNIX EGREP EJECT FALLOCATE FGREP FILE FIND \
    FLOCK FREE FSFREEZE GREP HELP HEXEDIT HOSTNAME HWCLOCK IFCONFIG \
    INSMOD IONICE IOTOP KILL KILLALL LOGIN LOSETUP LSATTR LSMOD LSPCI \
    LSUSB MKPASSWD MKSWAP MODINFO MOUNT MOUNTPOINT NC NETCAT NETSTAT \
    NSENTER PARTPROBE PASSWD PATCH PGREP PIDOF PIVOT_ROOT PKILL PMAP \
    PS PWDX READAHEAD REBOOT RENICE RESET REV RFKILL RMMOD SED SETSID \
    STRINGS SU SWAPOFF SWAPON SWITCH_ROOT SYSCTL TASKSET TIME TOP ULIMIT \
    UMOUNT UNIX2DOS UNSHAR EUPTIME USLEEP UUDECODE UUENCODE VCONFIG VMSTAT \
    W WHICH XARGS XXD; do
    sed -i -e "s,^CONFIG_$i=.*,CONFIG_$i=n," .config
done

%build
%make

%install
PREFIX="%{buildroot}" scripts/install.sh --symlink --force --long

%files
/bin/*
/sbin/*
%{_bindir}/*
%{_sbindir}/*
