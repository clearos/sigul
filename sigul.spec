# FIXME: eventually migrate from sysv to systemd service configuration
Summary: A signing server and related software client
Name: sigul
Version: 0.100
Release: 6%{?dist}
License: GPLv2
Group: Applications/Internet
URL: https://fedorahosted.org/sigul/
Source0: https://fedorahosted.org/releases/s/i/sigul/sigul-%{version}.tar.bz2
Source1: sigul_bridge.init
Source2: sigul_server.init
Source3: sigul.logrotate
Requires: gnupg, koji, logrotate, pexpect, pygpgme, python, python-fedora,
Requires: python-nss >= 0.11
Requires: python-sqlalchemy >= 0.5
Requires: python-urlgrabber
Requires: rpm-sign
%if 0%{?rhel} && 0%{?rhel} <= 5
Requires: python-sqlite2
%endif
# For sigul_setup_client
Requires: coreutils nss-tools
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig, initscripts
Requires(postun): initscripts
BuildRequires: python
# To detect the path correctly in configure
BuildRequires: gnupg
BuildArch: noarch

%description
A signing server, which lets authorized users sign data without having any
access to the necessary private key, a client for the server, and a "bridge"
that connects the two.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install
mkdir -p $RPM_BUILD_ROOT%{_initrddir} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/sigul_bridge
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/sigul_server
install -m 0644 -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sigul

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group sigul >/dev/null || groupadd -r sigul
getent passwd sigul >/dev/null || \
useradd -r -g sigul -d %{_localstatedir}/lib/sigul -s /sbin/nologin \
        -c "Signing server or bridge" sigul
exit 0

%post
/sbin/chkconfig --add sigul_bridge
/sbin/chkconfig --add sigul_server

%preun
if [ "$1" = 0 ]; then
   /sbin/service sigul_bridge stop >/dev/null 2>&1
   /sbin/service sigul_server stop >/dev/null 2>&1
   /sbin/chkconfig --del sigul_bridge
   /sbin/chkconfig --del sigul_server
fi

%postun
if [ "$1" -ge 1 ]; then
   /sbin/service sigul_bridge condrestart >/dev/null 2>&1 || :
   /sbin/service sigul_server condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%dir %{_sysconfdir}/sigul
%config(noreplace) %{_sysconfdir}/sigul/client.conf
%config(noreplace) %attr(640,root,sigul) %{_sysconfdir}/sigul/bridge.conf
%config(noreplace) %attr(640,root,sigul) %{_sysconfdir}/sigul/server.conf
%{_initrddir}/sigul*
%config(noreplace) %{_sysconfdir}/logrotate.d/sigul
%{_bindir}/sigul*
%{_sbindir}/sigul*
%{_mandir}/man1/sigul*.1*
%{_mandir}/man8/sigul*.8*
%{_datadir}/sigul
%dir %attr(700,sigul,sigul) %{_localstatedir}/lib/sigul
%dir %attr(700,sigul,sigul) %{_localstatedir}/lib/sigul/gnupg

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Miloslav Trmač <mitr@redhat.com> - 0.100-5
- Add Requires: rpm-sign
  Resolves: #1215678

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Miloslav Trmač <mitr@redhat.com> - 0.100-1
- Update to sigul-0.100.

* Wed Feb  8 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.99-3
- Remove the python-sqlite2 dep in Fedora as that package is being retired and
  sigul can use the sqlite3  module from the python stdlib

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun  6 2011 Miloslav Trmač <mitr@redhat.com> - 0.99-1
- Update to sigul-0.99.

* Thu Jun  2 2011 Miloslav Trmač <mitr@redhat.com> - 0.98-2
- Add Requires: gnupg
  Resolves: #664536

* Tue May 31 2011 Miloslav Trmač <mitr@redhat.com> - 0.98-1
- Update to sigul-0.98.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com>
- recompiling .py files against Python 2.7 (rhbz#623359)

- Drop no longer necessary references to BuildRoot:

* Fri Jul 31 2009 Miloslav Trmač <mitr@redhat.com> - 0.97-1
- Update to sigul-0.97.
- Ship NEWS.

* Tue Jul 28 2009 Jesse Keating <jkeating@redhat.com> - 0.96-6
- Fix the patch in -4

* Tue Jul 28 2009 Jesse Keating <jkeating@redhat.com> - 0.96-5
- Add a dist tag

* Tue Jul 28 2009 Jesse Keating <jkeating@redhat.com> - 0.96-4
- Add another patch to temporarily work around a stale koji issue.
- Bump python-nss reqs up now that we have a newer one in EPEL

* Mon Jul 27 2009 Jesse Keating <jkeating@redhat.com> - 0.96-3
- Setup the Requires right for EL5

* Mon Jul 27 2009 Jesse Keating <jkeating@redhat.com> - 0.96-2
- Fix various bugs while testing (release by Mitr)
- Patch from jkeating for srpm signing.

* Sat Jul 18 2009 Miloslav Trmač <mitr@redhat.com> - 0.95-0.mitr.1
- Update to 0.95.
- Add missing Requires: m2crypto.

* Wed Jul  1 2009 Miloslav Trmač <mitr@redhat.com> - 0.94-0.mitr.1
- Update to 0.94.

* Fri Apr 10 2009 Miloslav Trmač <mitr@redhat.com> - 0.93-0.mitr.1
- Update to 0.93.

* Wed Jan 28 2009 Miloslav Trmač <mitr@redhat.com> - 0.92-0.mitr.1
- Update to 0.92.

* Mon Jan 12 2009 Miloslav Trmač <mitr@redhat.com> - 0.91-0.mitr.1
- Update to 0.91.

* Sun Jan 11 2009 Miloslav Trmač <mitr@redhat.com> - 0.90-0.mitr.2
- Requires: koji, python-sqlite2

* Sun Jan 11 2009 Miloslav Trmač <mitr@redhat.com> - 0.90-0.mitr.1
- s/rpmsigner/sigul/g

* Sun Nov 30 2008 Miloslav Trmač <mitr@redhat.com> - 0.90-0.mitr.1
- Initial package.
