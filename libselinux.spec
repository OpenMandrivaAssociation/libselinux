%define major 1
%define libnameold %mklibname selinux 1
%define libname        %mklibname selinux %{major}
%define libnamedevel %mklibname selinux -d
%define libnamestaticdevel %mklibname selinux -d -s

Name:           libselinux
Version:        2.0.77
Release:        %mkrel 1
Summary:        SELinux library and simple utilities
License:        Public Domain
Group:          System/Libraries
URL:            http://www.nsa.gov/selinux/
Source0:        http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
#Source1:        http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz.sign
Patch0:         libselinux-rhat.patch
BuildRequires:  sepol-static-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
Summary:        SELinux library and simple utilities
Group:          System/Libraries
Provides:       libselinux = %{version}-%{release}
Provides:       selinux = %{version}-%{release}

%description -n %{libname}
libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions. Required for any applications that use the SELinux API.

%package -n %{libnamedevel}
Summary:        Development libraries and header files for %{name}
Group:          Development/C
Provides:       selinux-devel = %{version}-%{release}
Requires:       %{libname} = %{version}-%{release}
Obsoletes:      %{libnameold}-devel < %{version}-%{release}

%description -n %{libnamedevel}
The selinux-devel package contains the libraries and header
files needed for developing SELinux applications.

%package -n %{libnamestaticdevel}
Summary:        Static development libraries for %{name}
Group:          Development/C
Provides:       selinux-static-devel = %{version}-%{release}
Requires:       %{libnamedevel} = %{version}-%{release}

%description -n %{libnamestaticdevel}
The selinux-static-devel package contains the static libraries
needed for developing SELinux applications.

%package utils
Summary:        Utilities for %{name}
Group:          System/Kernel and hardware

%description utils
This package contains numerous applications utilizing %{name}.

%package -n python-selinux
Summary:        Python bindings for %{name}
Group:          Development/Python
%py_requires -d

%description -n python-selinux
This package contains python bindings for %{name}.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
    CFLAGS="%{optflags}" \
    LIBDIR=%{_libdir} \
    PYLIBVER=%{py_ver} \
    PYINC=%{py_incdir} \
    PYLIB=%{py_platsitedir} \
    PYTHONLIBDIR="%{py_platsitedir}" \
    all pywrap

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}/%{_lib}
install -d %{buildroot}%{_mandir}/man3

%{make} \
    DESTDIR=%{buildroot} \
    LIBDIR="%{buildroot}%{_libdir}" \
    SHLIBDIR="%{buildroot}/%{_lib}" \
    install install-pywrap

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libselinux.so.*

%files utils
%defattr(-,root,root)
%doc ChangeLog LICENSE
%{_sbindir}/*
/sbin/matchpathcon
%{_mandir}/man?/*

%files -n %{libnamedevel}
%defattr(-,root,root)
%{_includedir}/selinux/*.h
%{_libdir}/*.so

%files -n %{libnamestaticdevel}
%defattr(-,root,root)
%{_libdir}/*.a

%files -n python-selinux
%defattr(-,root,root)
%{py_platsitedir}/*
