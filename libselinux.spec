%define major 1
%define libnameold %mklibname selinux 1
%define libname        %mklibname selinux %{major}
%define libnamedevel %mklibname selinux -d
%define libnamestaticdevel %mklibname selinux -d -s

Name:           libselinux
Version:        2.0.78
Release:        %mkrel 6
Summary:        SELinux library and simple utilities
License:        Public Domain
Group:          System/Libraries
URL:            http://www.nsa.gov/selinux/
Source0:        http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
#Source1:        http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz.sign
Patch0:         libselinux-rhat.patch
Patch1:		libselinux-2.0.78-fix-build.patch
BuildRequires:  sepol-static-devel

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
%patch1 -p0 -b .build

%build
%{__make} \
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

%{make} \
    DESTDIR=%{buildroot} \
    LIBDIR="%{buildroot}%{_libdir}" \
    SHLIBDIR="%{buildroot}/%{_lib}" \
    install install-pywrap

%files -n %{libname}
/%{_lib}/libselinux.so.*

%files utils
%doc ChangeLog LICENSE
%{_sbindir}/*
/sbin/matchpathcon
%{_mandir}/man?/*

%files -n %{libnamedevel}
%{_includedir}/selinux/*.h
%{_libdir}/*.so

%files -n %{libnamestaticdevel}
%{_libdir}/*.a

%files -n python-selinux
%{py_platsitedir}/*


%changelog
* Fri Nov 12 2010 Funda Wang <fwang@mandriva.org> 2.0.78-3mdv2011.0
+ Revision: 596436
- fix build

* Sun Sep 13 2009 Thierry Vignaud <tv@mandriva.org> 2.0.78-2mdv2010.0
+ Revision: 438737
- rebuild

* Fri Mar 06 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.78-1mdv2009.1
+ Revision: 349887
- New upstream release

* Thu Jan 15 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.77-1mdv2009.1
+ Revision: 329813
- New upstream release

* Sun Jan 04 2009 Funda Wang <fwang@mandriva.org> 2.0.76-2mdv2009.1
+ Revision: 324113
- rebuild

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.76-1mdv2009.1
+ Revision: 324069
- New upstream release

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.65-1mdv2009.1
+ Revision: 324051
- New upstream release

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 2.0.61-2mdv2009.0
+ Revision: 267992
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Apr 21 2008 David Walluck <walluck@mandriva.org> 2.0.61-1mdv2009.0
+ Revision: 196090
- fix build
- 2.0.61

* Wed Jan 02 2008 David Walluck <walluck@mandriva.org> 2.0.35-1mdv2008.1
+ Revision: 140263
- 2.0.35
- tabs to spaces
- enable parallel make

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 04 2007 David Walluck <walluck@mandriva.org> 2.0.8-5mdv2008.0
+ Revision: 79171
- fix Provides
- fix major on Obsolete devel package

* Mon Sep 03 2007 David Walluck <walluck@mandriva.org> 2.0.8-3mdv2008.0
+ Revision: 78475
- move %%py_requires -d to python-selinux subpackage

* Mon Sep 03 2007 David Walluck <walluck@mandriva.org> 2.0.8-2mdv2008.0
+ Revision: 78469
- Obsoletes: %%{libname}-devel < %%{version}-%%{release}
- fix static-devel Provides

* Sun Sep 02 2007 David Walluck <walluck@mandriva.org> 2.0.8-1mdv2008.0
+ Revision: 78367
- 2.0.8
- use python macros
- new lib policy
- do not use parallel make

* Sat Aug 11 2007 David Walluck <walluck@mandriva.org> 1.28-2mdv2008.0
+ Revision: 61847
- Provides: selinux-devel

  + Thierry Vignaud <tv@mandriva.org>
    - Import libselinux



* Thu Dec 22 2005 Oden Eriksson <oeriksson@mandriva.com> 1.28-1mdk
- 1.28
- fix deps
- added the python-selinux sub package

* Wed Mar 02 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.21.11-1mdk
- 1.21.11

* Thu Feb 17 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.21.9-1mdk
- 1.21.9
- sync with fedora patch

* Tue Feb 01 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.21.4-1mdk
- 1.21.4
- drop useless provides

* Thu Jan 13 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.20.1-1mdk
- 1.20.1

* Mon Jan 03 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.19.4-1mdk
- 1.19.4

* Fri Dec 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.19.3-1mdk
- 1.19.3
- drop P0

* Thu Dec 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.19.1-1mdk
- 1.19.1
- sync with fedora patch

* Wed Nov 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.18-1mdk
- 1.18

* Wed Aug 18 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.15.4-2mdk
- fix provides

* Wed Aug 18 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.15.4-1mdk
- 1.15.4
- sync patch with fedora
- drop useless-explicit-provides

* Sun Jul 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.15.1-1mdk
- 1.15.1

* Wed Jul 14 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.14.1-1mdk
- 1.14.1
- drop P1 (merged upstream)

* Tue Jun 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.13.4-1mdk
- 1.13.4
- drop P0 (merged upstream)
- add nlclass patch (P1 from fedora)

* Wed Jun 16 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.13.3-1mdk
- 1.13.3
- update P0 from fedora
- add man pages

* Thu Dec 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4-1mdk
- initial cooker contrib
- ripped parts from fedora, but adapted for mandrake
