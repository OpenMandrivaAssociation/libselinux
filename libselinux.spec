%define major 1
%define libname %mklibname selinux %{major}
%define devname %mklibname selinux -d
%define statname %mklibname selinux -d -s

%define _disable_ld_no_undefined 1
%define _disable_lto 1
%define _rundir /run

Summary:	SELinux library and simple utilities
Name:		libselinux
Version:	3.0
Release:	1
Epoch:		1
License:	Public Domain
Group:		System/Libraries
Url:		https://github.com/SELinuxProject/selinux/wiki
Source0:	https://github.com/SELinuxProject/selinux/releases/download/20191204/%{name}-%{version}.tar.gz
Source1:	selinuxconlist.8
Source2:	selinuxdefcon.8

BuildRequires:	sepol-static-devel swig
BuildRequires:	systemd
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libpcre2-posix)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(python2)

%description
Security-enhanced Linux is a patch of the Linux® kernel and a
number of utilities with enhanced security functionality designed
to add mandatory access controls to Linux. The Security-enhanced
Linux kernel contains new architectural components originally
developed to improve the security of the Flask operating system.
These architectural components provide general support for the
enforcement of many kinds of mandatory access control policies,
including those based on the concepts of Type Enforcement®,
Role-based Access Control, and Multi-level Security.

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions. Required for any applications that use the SELinux API.

%package -n %{libname}
Summary:	SELinux library and simple utilities
Group:		System/Libraries
Provides:	libselinux = %{EVRD}
Provides:	selinux = %{EVRD}

%description -n %{libname}
libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions. Required for any applications that use the SELinux API.

%package -n %{devname}
Summary:	Development libraries and header files for %{name}
Group:		Development/C
Provides:	selinux-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
The selinux-devel package contains the libraries and header
files needed for developing SELinux applications.

%package -n %{statname}
Summary:	Static development libraries for %{name}
Group:		Development/C
Provides:	selinux-static-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{statname}
The selinux-static-devel package contains the static libraries
needed for developing SELinux applications.

%package utils
Summary:	Utilities for %{name}
Provides:	selinux-utils = %{EVRD}
Group:		System/Kernel and hardware

%description utils
This package contains numerous applications utilizing %{name}.

%package -n	python3-libselinux
Summary:	SELinux python bindings for libselinux
Requires:	%{libname} = %{EVRD}
Provides:	python-libselinux = %{EVRD}
BuildRequires:	pkgconfig(python3)

%description -n python3-libselinux
The libselinux-python package contains the python bindings for developing
SELinux applications.

%package -n	python2-selinux
Summary:	Python 2 bindings for %{name}
Group:		Development/Python
Provides:	%{name}-python
BuildRequires:	pkgconfig(python2)

%description -n python2-selinux
This package contains python 2 bindings for %{name}.

%package -n ruby-selinux
Summary:	SELinux ruby bindings for libselinux
Group:		Development/Ruby
BuildRequires:	pkgconfig(ruby)

%description -n ruby-selinux
The libselinux-ruby package contains the ruby bindings for developing 
SELinux applications. 

%prep
%autosetup -p 2 -n libselinux-%{version}

# clang doesnt support these options
sed -i 's/-mno-tls-direct-seg-refs//' src/Makefile
sed -i 's/-fipa-pure-const//' src/Makefile utils/Makefile

%build
%serverbuild_hardened
export DISABLE_RPM="y"
export USE_PCRE2="y"

#export CFLAGS="$CFLAGS -DOVERRIDE_GETTID=0"

# To support building the Python wrapper against multiple Python runtimes
# Define a function, for how to perform a "build" of the python wrapper against
# a specific runtime:
BuildPythonWrapper() {
  BinaryName=$1

  # Perform the build from the upstream Makefile:
  make \
    CC=%{__cc} \
    PYTHON=$BinaryName \
    LIBDIR="%{_libdir}" %{?_smp_mflags} \
    pywrap
}

%make_build CC=%{__cc} clean
%make_build CC=%{__cc} LIBDIR="%{_libdir}" swigify
%make_build CC=%{__cc} LIBDIR="%{_libdir}" LDFLAGS="%{ldflags}" PYTHON=%{__python} all

BuildPythonWrapper %{__python2}
BuildPythonWrapper %{__python3}

%make_build SHLIBDIR="%{_libdir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" rubywrap


%install
InstallPythonWrapper() {
  BinaryName=$1

  make \
    PYTHON=$BinaryName \
    LIBDIR="%{_libdir}" %{?_smp_mflags} \
    LIBSEPOLA="%{_libdir}/libsepol.a" \
    pywrap

  make \
    PYTHON=$BinaryName \
    DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" \
    SHLIBDIR="%{_lib}" BINDIR="%{_bindir}" \
    SBINDIR="%{_sbindir}" \
    LIBSEPOLA="%{_libdir}/libsepol.a" \
    install-pywrap
}

rm -rf %{buildroot}
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}%{_rundir}/setrans
echo "d %{_rundir}/setrans 0755 root root" > %{buildroot}%{_tmpfilesdir}/libselinux.conf

InstallPythonWrapper %{__python2}
InstallPythonWrapper %{__python3}

make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" RUBYINSTALL=%{ruby_vendorarchdir} install install-rubywrap
# Nuke the files we don't want to distribute
rm -f %{buildroot}%{_sbindir}/compute_*
rm -f %{buildroot}%{_sbindir}/deftype
rm -f %{buildroot}%{_sbindir}/execcon
rm -f %{buildroot}%{_sbindir}/getenforcemode
rm -f %{buildroot}%{_sbindir}/getfilecon
rm -f %{buildroot}%{_sbindir}/getpidcon
rm -f %{buildroot}%{_sbindir}/mkdircon
rm -f %{buildroot}%{_sbindir}/policyvers
rm -f %{buildroot}%{_sbindir}/setfilecon
rm -f %{buildroot}%{_sbindir}/selinuxconfig
rm -f %{buildroot}%{_sbindir}/selinuxdisable
rm -f %{buildroot}%{_sbindir}/getseuser
rm -f %{buildroot}%{_sbindir}/togglesebool
rm -f %{buildroot}%{_sbindir}/selinux_check_securetty_context
mv %{buildroot}%{_sbindir}/getdefaultcon %{buildroot}%{_sbindir}/selinuxdefcon
mv %{buildroot}%{_sbindir}/getconlist %{buildroot}%{_sbindir}/selinuxconlist
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/
rm -f %{buildroot}%{_mandir}/man8/togglesebool*

%files utils
%doc LICENSE
%{_sbindir}/*
%{_mandir}/man[58]/*
%{_mandir}/ru/man*/*
%ghost %{_rundir}/setrans
%{_tmpfilesdir}/libselinux.conf

%files -n %{libname}
%{_libdir}/libselinux.so.%{major}*

%files -n %{devname}
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_mandir}/man3/*

%files -n %{statname}
%{_libdir}/libselinux.a

%files -n python2-selinux
%dir %{python2_sitearch}/selinux
%{python2_sitearch}/selinux/*.py*
%{python2_sitearch}/selinux/*.so
%{python2_sitearch}/*.so
%{python2_sitearch}/selinux-%{version}-py%{py2_ver}.egg-info

%files -n python3-libselinux
%{python3_sitearch}/selinux/
%{python3_sitearch}/selinux-%{version}-*
%{python3_sitearch}/_selinux.*

%files -n ruby-selinux
%{ruby_vendorarchdir}/selinux.so
