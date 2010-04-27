%define distro redhat
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MINIMUM:0}%{!?BUILD_MINIMUM:1}
%define BUILD_MINIMUM 1
%endif
%if %{?BUILD_OLPC:0}%{!?BUILD_OLPC:1}
%define BUILD_OLPC 0
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 1
%endif
%define POLICYVER 24
%define libsepolver 2.0.41-1
%define POLICYCOREUTILSVER 2.0.78-1
%define CHECKPOLICYVER 2.0.21-1
Summary: SELinux policy configuration
Name: selinux-policy
Version: 3.7.19
Release: 6.2%{?dist}
License: GPLv2+
Group: System Environment/Base
Source: refpolicy-%{version}.tar.gz
patch: refpolicy-%{version}.patch

Url: http://oss.tresys.com/repos/refpolicy/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python gawk checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils-python >= %{POLICYCOREUTILSVER} bzip2 
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER} libsemanage >= 2.0.14-3
Requires(post): /usr/bin/bunzip2 /bin/mktemp /bin/awk
Requires: checkpolicy >= %{CHECKPOLICYVER} m4 
Obsoletes: selinux-policy-devel <= %{version}-%{release}
Provides: selinux-policy-devel = %{version}-%{release}

%description 
SELinux Base package

%files 
%defattr(-,root,root,-)
%{_mandir}/man*/*
# policycoreutils owns these manpage directories, we only own the files within them
%{_mandir}/ru/*/*
%dir %{_usr}/share/selinux
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%dir %{_usr}/share/selinux/packages
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/policygentool
%{_usr}/share/selinux/devel/example.*
%{_usr}/share/selinux/devel/policy.*

%package doc
Summary: SELinux policy documentation
Group: System Environment/Base
Requires(pre): selinux-policy = %{version}-%{release}
Requires: /usr/bin/xdg-open

%description doc
SELinux policy documentation package

%files doc
%defattr(-,root,root,-)
%doc %{_usr}/share/doc/%{name}-%{version}
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp

%check
/usr/bin/sepolgen-ifgen -i %{buildroot}%{_usr}/share/selinux/devel/include -o /dev/null

%define makeCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 bare \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024  conf \
cp -f redhat/modules-%1.conf  ./policy/modules.conf \
cp -f redhat/booleans-%1.conf ./policy/booleans.conf \
cp -f redhat/users-%1 ./policy/users \

%define installCmds() \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 base.pp \
make validate UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 modules \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install \
make UNK_PERMS=%5 NAME=%1 TYPE=%2 DISTRO=%{distro} UBAC=n DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
#%{__cp} *.pp %{buildroot}/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 redhat/securetty_types-%1 %{buildroot}%{_sysconfdir}/selinux/%1/contexts/securetty_types \
install -m0644 redhat/setrans-%1.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
install -m0644 redhat/customizable_types %{buildroot}%{_sysconfdir}/selinux/%1/contexts/customizable_types \
bzip2 %{buildroot}/%{_usr}/share/selinux/%1/*.pp \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "%%s.pp.bz2 ", $1 }' ./policy/modules.conf > %{buildroot}/%{_usr}/share/selinux/%1/modules.lst
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp.bz2 \
%{_usr}/share/selinux/%1/modules.lst \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/x_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_domain_context \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_image_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/root \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/guest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/xguest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/staff_u 

%define saveFileContext() \
if [ -s /etc/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi \
fi

%define loadpolicy() \
( cd /usr/share/selinux/%1; \
semodule -b base.pp.bz2 -i %2 -s %1; \
); \

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
selinuxenabled; \
if [ $? = 0  -a "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT}.pre ]; then \
     fixfiles -C ${FILE_CONTEXT}.pre restore; \
     restorecon -R /root /var/log /var/run /var/lib 2> /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; 

%description
SELinux Reference Policy - modular.
Based off of reference policy: Checked out revision  2.20091117

%build

%prep 
%setup -n refpolicy-%{version} -q
%patch -p1

%install
cd redhat; cp -r config ../
cd ../
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_mandir}
cp -R  man/* %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/{targeted,mls,minimum,modules}/

# Install devel
make clean
%if %{BUILD_TARGETED}
# Build targeted policy
# Commented out because only targeted ref policy currently builds
%makeCmds targeted mcs n y allow
%installCmds targeted mcs n y allow
%endif

%if %{BUILD_MINIMUM}
# Build minimum policy
# Commented out because only minimum ref policy currently builds
%makeCmds minimum mcs n y allow
%installCmds minimum mcs n y allow
%endif

%if %{BUILD_MLS}
# Build mls policy
%makeCmds mls mls n y deny
%installCmds mls mls n y deny
%endif

%if %{BUILD_OLPC}
# Build olpc policy
# Commented out because only olpc ref policy currently builds
%makeCmds olpc mcs n y allow
%installCmds olpc mcs n y allow
%endif

make UNK_PERMS=allow NAME=targeted TYPE=mcs DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name}-%{version} POLY=y MLS_CATS=1024 MCS_CATS=1024 install-headers install-docs
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mkdir %{buildroot}%{_usr}/share/selinux/packages/
mv %{buildroot}%{_usr}/share/selinux/targeted/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 755 redhat/policygentool %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 redhat/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 doc/policy.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "xdg-open file:///usr/share/doc/selinux-policy-%{version}/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp
# rm -rf selinux_config
%clean
%{__rm} -fR %{buildroot}

%post
if [ ! -s /etc/selinux/config ]; then
#
#     New install so we will default to targeted policy
#
echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#     targeted - Targeted processes are protected,
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted 

" > /etc/selinux/config

     ln -sf ../selinux/config /etc/sysconfig/selinux 
     restorecon /etc/selinux/config 2> /dev/null || :
else
     . /etc/selinux/config
     # if first time update booleans.local needs to be copied to sandbox
     [ -f /etc/selinux/${SELINUXTYPE}/booleans.local ] && mv /etc/selinux/${SELINUXTYPE}/booleans.local /etc/selinux/targeted/modules/active/
     [ -f /etc/selinux/${SELINUXTYPE}/seusers ] && cp -f /etc/selinux/${SELINUXTYPE}/seusers /etc/selinux/${SELINUXTYPE}/modules/active/seusers
fi
exit 0

%postun
if [ $1 = 0 ]; then
     setenforce 0 2> /dev/null
     if [ ! -s /etc/selinux/config ]; then
          echo "SELINUX=disabled" > /etc/selinux/config
     else
          sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
     fi
fi
exit 0

%if %{BUILD_TARGETED}
%package targeted
Summary: SELinux targeted base policy
Provides: selinux-policy-base = %{version}-%{release}
Group: System Environment/Base
Obsoletes: selinux-policy-targeted-sources < 2
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  audispd-plugins <= 1.7.7-1
Obsoletes: mod_fcgid-selinux <= %{version}-%{release}
Conflicts:  seedit

%description targeted
SELinux Reference policy targeted base module.

%pre targeted
%saveFileContext targeted

%post targeted
packages=`cat /usr/share/selinux/targeted/modules.lst`
if [ $1 -eq 1 ]; then
   %loadpolicy targeted $packages
   restorecon -R /root /var/log /var/run /var/lib 2> /dev/null
else
   semodule -n -s targeted -r moilscanner -r mailscanner -r gamin -r audio_entropy -r iscsid -r polkit_auth -r polkit -r rtkit_daemon -r ModemManager 2>/dev/null
   %loadpolicy targeted $packages
   %relabel targeted
fi
exit 0

%triggerpostun targeted -- selinux-policy-targeted < 3.2.5-9.fc9
. /etc/selinux/config
[ "${SELINUXTYPE}" != "targeted" ] && exit 0
setsebool -P use_nfs_home_dirs=1
semanage user -l | grep -s unconfined_u > /dev/null
if [ $? -eq 0 ]; then
   semanage user -m -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u
else
   semanage user -a -P user -R "unconfined_r system_r" -r s0-s0:c0.c1023 unconfined_u
fi
seuser=`semanage login -l | grep __default__ | awk '{ print $2 }'`
[ "$seuser" != "unconfined_u" ]  && semanage login -m -s "unconfined_u"  -r s0-s0:c0.c1023 __default__
seuser=`semanage login -l | grep root | awk '{ print $2 }'`
[ "$seuser" = "system_u" ] && semanage login -m -s "unconfined_u"  -r s0-s0:c0.c1023 root
restorecon -R /root /etc/selinux/targeted 2> /dev/null
semodule -r qmail 2> /dev/null
exit 0

%files targeted
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/unconfined_u
%fileList targeted
%endif

%if %{BUILD_MINIMUM}
%package minimum
Summary: SELinux minimum base policy
Provides: selinux-policy-base = %{version}-%{release}
Group: System Environment/Base
Requires(post): policycoreutils-python >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description minimum
SELinux Reference policy minimum base module.

%pre minimum
%saveFileContext minimum

%post minimum
packages="execmem.pp.bz2 unconfined.pp.bz2 unconfineduser.pp.bz2"
%loadpolicy minimum $packages
if [ $1 -eq 1 ]; then
semanage -S minimum -i - << __eof
login -m  -s unconfined_u -r s0-s0:c0.c1023 __default__
login -m  -s unconfined_u -r s0-s0:c0.c1023 root
__eof
restorecon -R /root /var/log /var/run /var/lib 2> /dev/null
else
%relabel minimum
fi
exit 0

%files minimum
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/unconfined_u
%fileList minimum
%endif

%if %{BUILD_OLPC}
%package olpc 
Summary: SELinux olpc base policy
Group: System Environment/Base
Provides: selinux-policy-base = %{version}-%{release}
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description olpc 
SELinux Reference policy olpc base module.

%pre olpc 
%saveFileContext olpc

%post olpc 
packages=`cat /usr/share/selinux/olpc/modules.lst`
%loadpolicy olpc $packages

if [ $1 -ne 1 ]; then
%relabel olpc
fi
exit 0

%files olpc
%defattr(-,root,root,-)
%fileList olpc

%endif

%if %{BUILD_MLS}
%package mls 
Summary: SELinux mls base policy
Group: System Environment/Base
Provides: selinux-policy-base = %{version}-%{release}
Obsoletes: selinux-policy-mls-sources < 2
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER} setransd
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit

%description mls 
SELinux Reference policy mls base module.

%pre mls 
%saveFileContext mls

%post mls 
semodule -n -s mls -r mailscanner -r polkit -r ModemManager 2>/dev/null
packages=`cat /usr/share/selinux/mls/modules.lst`
%loadpolicy mls $packages

if [ $1 -eq 1 ]; then
   restorecon -R /root /var/log /var/run /var/lib 2> /dev/null
else
%relabel mls
fi
exit 0

%files mls
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/selinux/mls/contexts/users/unconfined_u
%fileList mls

%endif

%changelog
* Tue Apr 27 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-6.2
- Merge branch refpolicy.

* Tue Apr 27 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-6.1
- Merge branch Fedora (v3.7.19-6)

* Mon Apr 26 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-5.2
- Merge branch refpolicy.

* Mon Apr 26 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-5.1
- Fix changelog entry format
- Merge branch fedora (v.3.7.19-5)

* Sat Apr 24 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-4.3
- Merge refpolicy branch.
- allow xwindow users to search xdm var lib and read xdm var lib file so that they can display ".face" icon in tray.
- allow gpg_agent_t to read reneric usr files ( gpg --edit-key XXXX passwd)
- allow vino to search home root dir and to append xdm home files
- allow tmw to append xdm home files

* Sat Apr 24 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-4.2
- remove files_read_config_files from files_read_etc_files since thats for generic etc_t files only
- Initial cgclear policy
- allow insmod to list inotifyfs
- allow gpg to append to xdm home files
- allow lvm to rw unconfined sem.
- allow mutt pgpewrap to search home
- allow pulseaudio to read tmw tmpfs files
- allow tmw to signull all domains
- create unconfined_rw_sem()
- comment out userdom_append_inherited_user_home_files and tmp files for all daemons.

* Thu Apr 22 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-4.1
- Merge branch fedora (v3.7.19-4)
- Add fc spec for clamd executable optional location.

* Wed Apr 21 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-2.3
- irc, irssi: add support for SSL connection to Freenode

* Tue Apr 20 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-2.2
- Merge refpolicy branch.

* Wed Apr 14 2010 Dominick Grift <dgrift@gmail.com> 3.7.19-2.1
- Merge branch fedora (v3.7.19-2)

* Wed Apr 14 2010 Dominick Grift <dgrift@gmail.com> 3.7.18-3.1
- Merge branch fedora (v3.7.18-3) except apps/telepathysofiasip.
- Run munin_t with SystemLow-SystemHigh if MCS is enabled.
- Implement cbp comments for irc (irssi) policy.

* Tue Apr 13 2010 Dominick Grift <dgrift@gmail.com> 3.7.18-1.3
- readd a port declaration removed by refpolicy merge.
- cleaned up some port ranges.
- Merge branch refpolicy.
- undo cgroup fixes for now.

* Tue Apr 13 2010 Dominick Grift <dgrift@gmail.com> 3.7.18-1.2
- cgroup fixes.

* Tue Apr 13 2010 Dominick Grift <dgrift@gmail.com> 3.7.18-1.1
- Merge branch Fedora (v3.7.18-1)

* Tue Apr 06 2010 Dominick Grift <dgrift@gmail.com> 3.7.17-6.1
- Merge branch refpolicy.
- Merge branch fedora (3.7.17-6)
- Various fixes.

* Fri Apr 02 2010 Dominick Grift <dgrift@gmail.com> 3.7.17-5.1
- Merge fedora branch (3.7.17-5)
- Fixed an error i made whilst merging fedora branch.
- Changed cgroup dir interface calls in userdomain and virt to just search.

* Wed Mar 31 2010 Dominick Grift <dgrift@gmail.com> 3.7.17-3.1
- Merge fedora branch (3.7.17-3)
- Create cgroup dir interfaces.
- added various cgroup dir interface calls (virt, userdomain, init).

* Wed Mar 31 2010 Dominick Grift <dgrift@gmail.com> 3.7.17-2.3
- Integrate my scripts into new dgrifts_scripts module.
- Call dgrifts_scripts_role for common users.
- Install dgrifts_scripts module.
- Allow plymouthd to use all ttys.
- Add various files to gitignore.

* Wed Mar 31 2010 Dominick Grift <dgrift@gmail.com> 3.7.17-2.2
- Integrate tmw policy into games module.
- Call games_role for unpriv users.
- Move some role_calls from common to unpriv users.
- Add nscd_socket_use calls to various modules.
- Declare tmw port tcp:6901
- Move user_$1_direct_dri to unpriv users.
- Allow by boolean rw_dri (compiz etc) per user domain.
- Allow nsplugin to set attributes of pulseaudio home dirs.
- Allow nsplugin to rw pulseaudio home lnk_files.
- Allow crond_t to list user_cron_spool_t dirs and to read user_cron_spool_t files.
- Allow unpriv user to list cgroup dirs.

* Tue Mar 30 2010 Dominick Grift <dgrift@gmail.com> 3.7.17-2.1
- Merge fedora branch (3.7.17-2)

* Tue Mar 30 2010 Dominick Grift <dgrift@gmail.com> 3.7.16-2.2
- Fixing syntax errors and other weird compiler issues in various modules.
- Fix a string error on denyhosts_admin.
- Fix vino_role call to include role prefix.
- policy/modules/services/nagios.te:321: Warning: libs_use_lib_files(nagios_mail_plugin_t) has been deprecated, use libs_use_shared_libs() instead.
- Integrate Seahorse policy and all dependencies.
- Call seahorse_role for common users.
- Install seahorse module.
- Mplayer fixes.
- Call mplayer_role for common users,
- Integrate telepathy and vino policy and all its dependencies.
- Call vino_role and telepathy_role_template for common users.
- Install vino and telepathy modules.
- Install oident module.
- Allow oidentd to request the kernel to load a module.
- All common users to manage and relabel oidentd user home content (~/.oidentd.conf).
- Integrate elink policy into new html module.
- Call elinks_role for common users.
- Install html module.
- Integrate my mutt policy into new mail module.
- Call mutt_role for common users.
- Allow gpg to sign and encrypt mutt e-mails.
- Install mail module.
- Integrate my irssi policy into irc module.
- Modified git policy to support automount.
- call irc_role and git_session_role for common users.
- Integrate my git differences.

* Mon Mar 29 2010 Dominick Grift <dgrift@gmail.com> 3.7.16-2.1
- Merge refpolicy.
- Merge fedora.
- Ignore .project.
- Cleanup denyhosts_admin.

* Sun Mar 28 2010 Dominick Grift <dgrift@gmail.com> 3.7.16-1.1
- Import 3.7.16-1.
- Fix spec to include patch for master branch.
- Comment out execmem_exec_t file context specifications for mutter and compiz. I dont need it.
