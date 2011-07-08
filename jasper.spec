
# NOTE: packages that can use jasper:
# ImageMagick
# netpbm

Summary: Implementation of the JPEG-2000 standard, Part 1
Name:    jasper
Group:   System Environment/Libraries
Version: 1.900.1
Release: 15%{?dist}

License: JasPer
URL:     http://www.ece.uvic.ca/~mdadams/jasper/
Source0: http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: jasper-1.701.0-GL.patch
# autoconf/automake bits of patch1
Patch2: jasper-1.701.0-GL-ac.patch
# CVE-2007-2721 (bug #240397)
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=413041;msg=88
Patch3: patch-libjasper-stepsizes-overflow.diff
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786 
Patch4: jpc_dec.c.patch
# OpenBSD hardening patches addressing couple of possible integer overflows
# during the memory allocations
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3520
Patch5: jasper-1.900.1-CVE-2008-3520.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3522
Patch6: jasper-1.900.1-CVE-2008-3522.patch
# add pkg-config support
Patch7: jasper-pkgconfig.patch

BuildRequires: automake libtool
BuildRequires: freeglut-devel 
BuildRequires: libGLU-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig

Requires: %{name}-libs = %{version}-%{release}

%description
This package contains an implementation of the image compression
standard JPEG-2000, Part 1. It consists of tools for conversion to and
from the JP2 and JPC formats.

%package devel
Summary: Header files, libraries and developer documentation
Group:   Development/Libraries
Provides: libjasper-devel = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: libjpeg-devel
Requires: pkgconfig
%description devel
%{summary}.

%package libs 
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Conflicts: jasper < 1.900.1-4
%description libs 
%{summary}.

%package utils 
Summary: Nonessential utilities for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%description utils 
%{summary}, including jiv and tmrdemo.



%prep
%setup -q -n %{name}-%{version}

%patch1 -p1 -b .GL
%patch2 -p1 -b .GL-ac
%patch3 -p1 -b .CVE-2007-2721
%patch4 -p1 -b .jpc_dec_assertion
%patch5 -p1 -b .CVE-2008-3520
%patch6 -p1 -b .CVE-2008-3522
%patch7 -p1 -b .pkgconfig

autoreconf -i


%build

%configure \
  --enable-shared \
  --disable-static 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Unpackaged files
rm -f doc/README
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYRIGHT LICENSE NEWS README
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%{_mandir}/man1/img*
%{_mandir}/man1/jasper.1*

%files devel
%defattr(-,root,root,-)
%doc doc/*
%{_includedir}/jasper/
%{_libdir}/libjasper.so
%{_libdir}/pkgconfig/jasper.pc

%files libs
%defattr(-,root,root,-)
%{_libdir}/libjasper.so.1*

%files utils
%defattr(-,root,root,-)
%{_bindir}/jiv
%{_bindir}/tmrdemo
%{_mandir}/man1/jiv.1*


%changelog
* Tue Mar 02 2010 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-15
- Move documentation from libs subpackage to main package

* Thu Oct 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-14
- add pkgconfig support

* Mon Oct 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-13
- CVE-2008-3520 jasper: multiple integer overflows in jas_alloc calls (#461476)
- CVE-2008-3522 jasper: possible buffer overflow in 
  jas_stream_printf() (#461478)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-11
- FTBFS jasper-1.900.1-10.fc11 (#511743)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Rex Dieter <rdieter@fedoraproject.org> 1.900.1-9
- patch for "jpc_dec_tiledecode: Assertion `dec->numcomps == 3' failed)
  (#481284, #481291)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.900.1-8
- respin (gcc43)

* Mon Oct 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-7
- -libs: %%post/%%postun -p /sbin/ldconfig

* Mon Sep 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-6
- -libs: -Requires: %%name
- -devel: +Provides: libjasper-devel
- drop (unused) geojasper bits

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-4
- -libs subpkg to be multilib friendlier
- -utils subpkg for non-essential binaries jiv, tmrdemo (#244153)

* Fri Aug 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-3
- License: JasPer

* Wed May 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-2
- CVE-2007-2721 (#240397)

* Thu Mar 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-1
- jasper-1.900.1

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.900.0-3
- omit deprecated memleak patch

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.900.0-2
- jasper-1.900.0 (#218947)

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-15
- memory leak (#207006)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-13
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-12
- fixup build issues introduced by geojasper integration

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-10
- support/use geojasper (optional, default no)
- fc5: gcc/glibc respin

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-9
- workaround "freeglut-devel should Requires: libGL-devel, libGLU-devel"
  (#179464)

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-8
- revert jasper to jaspertool rename (#176773)
- actually use/apply GL patch

* Tue Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-7
- GL patch to remove libGL dependancy (using only freeglut)

* Tue Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-6
- token %%check section
- --enable-shared 

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-5
- use %%{?dist}
- BR: libGL-devel 

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Oct 23 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.3
- Capitalize summary
- remove 0-length ChangeLog

* Fri Jun 04 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.2
- nuke .la file
- BR: glut-devel -> freeglut-devel

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.1
- 1.701.0

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.700.5-0.fdr.2
- avoid conflicts with fc'2 tomcat by renaming /usr/bin/jasper -> jaspertool

* Mon Mar 08 2004 Rex Dieter <rexdieter at sf.net> 0:1.700.5-0.fdr.1
- use Epochs.
- -devel: Requires: %%name = %%epoch:%%version

* Thu Jan 22 2004 Rex Dieter <rexdieter at sf.net> 1.700.5-0.fdr.0
- first try

