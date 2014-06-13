%define major 1
%define libname %mklibname selinux %{major}
%define devname %mklibname selinux -d
%define statname %mklibname selinux -d -s

Summary:	SELinux library and simple utilities
Name:		libselinux
Version:	2.0.78
Release:	11
License:	Public Domain
Group:		System/Libraries
Url:		http://www.nsa.gov/selinux/
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
#Source1:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz.sign
Patch0:		libselinux-rhat.patch
Patch1:		libselinux-2.0.78-fix-build.patch
BuildRequires:	sepol-static-devel

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
Summary:	Python bindings for %{name}
Group:		Development/Python
BuildRequires:  pkgconfig(python-2.7)

%description -n python-selinux
This package contains python bindings for %{name}.

%prep
%setup -q
%apply_patches

%build
%serverbuild_hardened
make \
	CFLAGS="%{optflags}" \
	LIBDIR=%{_libdir} \
	CC=%{__cc}	\
	LDFLAGS="%{ldflags}" \
	PYLIBVER=%{py_ver} \
	PYINC=%{py_incdir} \
	PYLIB=%{py_platsitedir} \
	PYTHONLIBDIR="%{py_platsitedir}" \
	all pywrap

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}/%{_lib}
install -d %{buildroot}%{_mandir}/man3

%make \
	DESTDIR=%{buildroot} \
	LIBDIR="%{buildroot}%{_libdir}" \
	SHLIBDIR="%{buildroot}/%{_lib}" \
	install install-pywrap

%files utils
%doc ChangeLog LICENSE
%{_sbindir}/*
/sbin/matchpathcon
%{_mandir}/man?/*

%files -n %{libname}
/%{_lib}/libselinux.so.%{major}*

%files -n %{devname}
%{_includedir}/selinux/*.h
%{_libdir}/*.so

%files -n %{statname}
%{_libdir}/*.a

%files -n python-selinux
%{py_platsitedir}/*

