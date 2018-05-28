%define major 1
%define libname %mklibname selinux %{major}
%define devname %mklibname selinux -d
%define statname %mklibname selinux -d -s

%define _disable_ld_no_undefined 1
%define _disable_lto 1

Summary:	SELinux library and simple utilities
Name:		libselinux
Version:	2.8
Release:	1
License:	Public Domain
Group:		System/Libraries
Url:		https://github.com/SELinuxProject/selinux/wiki
Source0:	https://github.com/SELinuxProject/selinux/releases/download/20180524/%{name}-%{version}.tar.gz
Source1:	selinuxconlist.8
Source2:	selinuxdefcon.8
BuildRequires:	sepol-static-devel swig
BuildRequires:	pkgconfig(liblzma) pkgconfig(libpcre)

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
Provides:	libselinux = %{version}-%{release}
Provides:	selinux = %{version}-%{release}

%description -n %{libname}
libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions. Required for any applications that use the SELinux API.

%package -n %{devname}
Summary:	Development libraries and header files for %{name}
Group:		Development/C
Provides:	selinux-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
The selinux-devel package contains the libraries and header
files needed for developing SELinux applications.

%package -n %{statname}
Summary:	Static development libraries for %{name}
Group:		Development/C
Provides:	selinux-static-devel = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}

%description -n %{statname}
The selinux-static-devel package contains the static libraries
needed for developing SELinux applications.

%package utils
Summary:	Utilities for %{name}
Group:		System/Kernel and hardware

%description utils
This package contains numerous applications utilizing %{name}.

%package -n python-selinux
Summary:	Python 3 bindings for %{name}
Group:		Development/Python
BuildRequires:	pkgconfig(python3)

%description -n python-selinux
This package contains python 3 bindings for %{name}.

%package -n ruby-selinux
Summary:	SELinux ruby bindings for libselinux
Group:		Development/Ruby
BuildRequires:	pkgconfig(ruby)
#Provides: ruby(selinux)

%description -n ruby-selinux
The libselinux-ruby package contains the ruby bindings for developing 
SELinux applications. 

%prep
%setup -q
%apply_patches

# clang doesnt support these options
sed -i 's/-mno-tls-direct-seg-refs//' src/Makefile
sed -i 's/-fipa-pure-const//' src/Makefile utils/Makefile

%build
%global optflags %{optflags} -Qunused-arguments

%serverbuild_hardened
%make swigify
%make \
	CFLAGS="%{optflags}" \
	LIBDIR=%{_libdir} \
	SHLIBDIR=/%{_lib} \
	CC=%{__cc} \
	LDFLAGS="%{ldflags}" \
	PYTHON=%__python3 \
	all pywrap rubywrap

%install
mkdir -p %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}/sbin/
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}/%{_lib}
install -d %{buildroot}%{_mandir}/man3
install -d %{buildroot}%{_rundir}/setrans
echo "d /run/setrans 0755 root root" > %{buildroot}%{_tmpfilesdir}/libselinux.conf


%makeinstall_std \
	LIBDIR="/%{_libdir}" \
	SHLIBDIR="/%{_lib}" \
	RUBYINSTALL="%{ruby_vendorarchdir}" \
	PYTHON=%__python3 \
	install-pywrap install-rubywrap
mv %{buildroot}%{_sbindir}/matchpathcon %{buildroot}/sbin/matchpathcon

# Nuke the files we don't want to distribute
rm %{buildroot}%{_sbindir}/compute_*
rm %{buildroot}%{_sbindir}/getfilecon
rm %{buildroot}%{_sbindir}/getpidcon
rm %{buildroot}%{_sbindir}/policyvers
rm %{buildroot}%{_sbindir}/setfilecon
rm %{buildroot}%{_sbindir}/getseuser
rm %{buildroot}%{_sbindir}/togglesebool
rm %{buildroot}%{_sbindir}/selinux_check_securetty_context
mv %{buildroot}%{_sbindir}/getdefaultcon %{buildroot}%{_sbindir}/selinuxdefcon
mv %{buildroot}%{_sbindir}/getconlist %{buildroot}%{_sbindir}/selinuxconlist
install -p -m644 %{SOURCE1} -D %{buildroot}%{_mandir}/man8/selinuxconlist.8
install -p -m644 %{SOURCE2} -D %{buildroot}%{_mandir}/man8/selinuxdefcon.8
rm %{buildroot}%{_mandir}/man8/togglesebool*

%files utils
%doc LICENSE
%{_sbindir}/*
/sbin/matchpathcon
%{_mandir}/man[58]/*
%ghost %{_rundir}/setrans
%{_tmpfilesdir}/libselinux.conf

%files -n %{libname}
/%{_lib}/libselinux.so.%{major}*

%files -n %{devname}
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_mandir}/man3/*

%files -n %{statname}
%{_libdir}/libselinux.a

%files -n python-selinux
%dir %{python_sitearch}/selinux
%{python_sitearch}/selinux/*.py*
%{python_sitearch}/selinux/*.so
%{python_sitearch}/_*.so

%files -n ruby-selinux
%{ruby_vendorarchdir}/selinux.so
