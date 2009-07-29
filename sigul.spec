Summary: A signing server and related software client
Name: sigul
Version: 0.96
Release: 6%{?dist}
License: GPLv2
Group: Applications/Internet
URL: https://fedorahosted.org/sigul/
# Source may not be uploaded yet
Source0: https://fedorahosted.org/releases/s/i/sigul/sigul-%{version}.tar.bz2
Source1: sigul_bridge.init
Source2: sigul_server.init
Source3: sigul.logrotate
Requires: koji, logrotate, m2crypto, pexpect, pygpgme, python, python-fedora,
Requires: python-nss >= 0.6
Requires: python-sqlalchemy, python-sqlite2
Requires: python-urlgrabber
# For sigul_setup_client
Requires: coreutils nss-tools
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig, initscripts
Requires(postun): initscripts
BuildRequires: python
# To detect the path correctly in configure
BuildRequires: gnupg
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Patch0: 0001-Handle-signing-of-source-rpms.patch
Patch1: 0002-Temporary-workaround-for-accidentially-re-downloadin.patch

%description
A signing server, which lets authorized users sign data without having any
access to the necessary private key, a client for the server, and a "bridge"
that connects the two.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1 

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
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
%doc AUTHORS COPYING README
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
