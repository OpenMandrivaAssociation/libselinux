%define	major 1
%define libname	%mklibname selinux %{major}

Summary:	SELinux library and simple utilities
Name:		libselinux
Version:	1.28
Release:	%mkrel 2
License:	Public Domain
Group:		System/Libraries
URL:		http://www.nsa.gov/selinux/
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
Source1:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz.sign
BuildRequires:	libsepol-devel
BuildRequires:	python-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{libname}
Summary:	SELinux library and simple utilities
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions. Required for any applications that use the SELinux API.

%package -n	%{libname}-devel
Summary:	Development libraries and header files
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:       selinux-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
The selinux-devel package contains the static libraries and header
files needed for developing SELinux applications. 

%package	utils
Summary:	Utilities for %{name}
Group:		System/Kernel and hardware

%description	utils
This package contains numerous applications utilizing %{name}.

%package -n	python-selinux
Summary:	Python bindings for %{name}
Group:		Development/Python

%description -n	python-selinux
This package contains python bindings for %{name}.

%prep

%setup -q

%build

%make \
    CFLAGS="%{optflags}" \
    LIBDIR="%{_libdir}" \
    PYLIBVER="python%{py_ver}" \
    PYINC="%{_includedir}/python%{py_ver}" \
    PYLIB="%{_libdir}/python%{py_ver}" \
    PYTHONLIBDIR="%{_libdir}/python%{py_ver}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir} 
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}/%{_lib} 
install -d %{buildroot}%{_mandir}/man3

%makeinstall_std \
    LIBDIR="%{buildroot}%{_libdir}" \
    SHLIBDIR="%{buildroot}/%{_lib}"

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libselinux.so.*

%files utils
%defattr(-,root,root)
%doc ChangeLog LICENSE
%{_sbindir}/*
%{_mandir}/man?/*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/selinux/*.h
%{_libdir}/*.so
%{_libdir}/*.a

%files -n python-selinux
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*
