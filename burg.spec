#
# TODO
# - burgemu notes
#   --enable-burg-emu-usb conflicts with --enable-burg-emu-pci, emu-pci seems experimental
#   - to build and install the `burg-emu' debugging utility we need to re-run build with --target=emu
#   - put burg-emu to subpackage if it is fixed
# - merge more from grub2.spec
# - desc
# - how to enable themes?
#
# Conditional build:
%bcond_with	burgemu		# build burg-emu debugging utility
#
%define		rev	r1844
Summary:	-
Summary(pl.UTF-8):	-
Name:		burg
Version:	1.98.%{rev}
Release:	0.%{rev}.1
License:	GPL v3+
Group:		Base
Source0:	%{name}-%{version}-bzr.tar.gz
# Source0-md5:	19b8ec2fe6208788bcf877c5a3b7e91d
Source3:	burg.sysconfig
Source4:	burg-custom.cfg
Patch0:		pld-initrd.patch
Patch1:		pld-sysconfdir.patch
Patch2:		%{name}-garbage.patch
Patch3:		%{name}-shelllib.patch
Patch4:		%{name}-install.in.patch
Patch5:		%{name}-lvmdevice.patch
Patch6:		pld-mkconfigdir.patch
# TODO: needs updates
Patch7:		%{name}-mkconfig-diagnostics.patch
URL:		https://launchpad.net/~bean123ch/+archive/burg
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gawk
BuildRequires:	help2man
BuildRequires:	ruby
BuildRequires:	texinfo
%ifarch %{ix86} %{x8664}
BuildRequires:	lzo-devel >= 1.0.2
%endif
%ifarch %{x8664}
BuildRequires:	/usr/lib/libc.so
%if "%{pld_release}" == "ac"
BuildRequires:	libgcc32
%else
BuildRequires:	gcc-multilib
%endif
%endif
BuildRequires:	ncurses-devel
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	which
Suggests:	cdrkit-mkisofs
Suggests:	os-prober
Provides:	bootloader
Conflicts:	grub
ExclusiveArch:	%{ix86} %{x8664} ppc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir        /sbin
%define		_bindir         %{_sbindir}
%define		_libdir		/boot
%define		_libexecdir	%{_libdir}/burg

%description

%description -l pl.UTF-8

%prep
%setup -q -n %{name}-%{version}-bzr
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
./autogen.sh
export CFLAGS="-Os %{?debug:-g}"
%configure \
%if %{with burgemu}
	--enable-grub-emu-usb \
	--enable-grub-emu-sdl \
	--enable-grub-emu-pci \
%endif
	BUILD_CFLAGS="$CFLAGS"
%{__make} -j1 \
	pkgdatadir=%{_libexecdir} \
	pkglibdir=%{_libexecdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{_sysconfdir}/burg.d}

%{__make} install \
	pkgdatadir=%{_libexecdir} \
	pkglibdir=%{_libexecdir} \
	DESTDIR=$RPM_BUILD_ROOT

cp -a docs/grub.cfg $RPM_BUILD_ROOT%{_libexecdir}
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/burg
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/burg.d/custom.cfg
cp -a grub-mkconfig_lib $RPM_BUILD_ROOT/lib/burg-mkconfig_lib
%{__rm} $RPM_BUILD_ROOT%{_infodir}/dir

# deprecated. we don't need it
%{__rm} $RPM_BUILD_ROOT/lib/update-burg_lib

# no junk to %{_libdir}/grub (put to -devel?)
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/*.h
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/*.mk

# core.img - bootable image generated by burg-mkimage(1) via burg-install(1)
touch $RPM_BUILD_ROOT%{_libexecdir}/core.img
touch $RPM_BUILD_ROOT%{_libexecdir}/device.map

%clean
rm -rf $RPM_BUILD_ROOT

%post -p %{_sbindir}/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun -p %{_sbindir}/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/burg
%attr(755,root,root) %{_sbindir}/burg-adduser
%attr(755,root,root) %{_sbindir}/burg-bin2h
%attr(755,root,root) %{_sbindir}/burg-deluser
%attr(755,root,root) %{_sbindir}/burg-editenv
%attr(755,root,root) %{_sbindir}/burg-fstest
%attr(755,root,root) %{_sbindir}/burg-install
%attr(755,root,root) %{_sbindir}/burg-mkconfig
%attr(755,root,root) %{_sbindir}/burg-mkelfimage
%attr(755,root,root) %{_sbindir}/burg-mkfont
%attr(755,root,root) %{_sbindir}/burg-mkimg
%attr(755,root,root) %{_sbindir}/burg-mkisofs
%attr(755,root,root) %{_sbindir}/burg-mkmod
%attr(755,root,root) %{_sbindir}/burg-mkpasswd-pbkdf2
%attr(755,root,root) %{_sbindir}/burg-mkrelpath
%attr(755,root,root) %{_sbindir}/burg-mkrescue
%attr(755,root,root) %{_sbindir}/burg-objdump
%attr(755,root,root) %{_sbindir}/burg-reboot
%attr(755,root,root) %{_sbindir}/burg-script-check
%attr(755,root,root) %{_sbindir}/burg-set-default
%attr(755,root,root) %{_sbindir}/burg-symdb
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_sbindir}/burg-mkimage
%{_mandir}/man1/burg-mkimage.1*
%else
%attr(755,root,root) %{_sbindir}/burg-probe
%attr(755,root,root) %{_sbindir}/burg-mkdevicemap
%{_mandir}/man8/burg-probe.8*
%{_mandir}/man8/burg-mkdevicemap.8*
%endif
%{_mandir}/man1/burg-bin2h.1*
%{_mandir}/man1/burg-editenv.1*
%{_mandir}/man1/burg-fstest.1*
%{_mandir}/man1/burg-mkelfimage.1*
%{_mandir}/man1/burg-mkfont.1*
%{_mandir}/man1/burg-mkimg.1*
%{_mandir}/man1/burg-mkisofs.1*
%{_mandir}/man1/burg-mkmod.1*
%{_mandir}/man1/burg-mkpasswd-pbkdf2.1*
%{_mandir}/man1/burg-mkrelpath.1*
%{_mandir}/man1/burg-mkrescue.1*
%{_mandir}/man1/burg-objdump.1*
%{_mandir}/man1/burg-script-check.1*
%{_mandir}/man1/burg-symdb.1*
%{_mandir}/man8/burg-adduser.8*
%{_mandir}/man8/burg-deluser.8*
%{_mandir}/man8/burg-install.8*
%{_mandir}/man8/burg-mkconfig.8*
%{_mandir}/man8/burg-reboot.8*
%{_mandir}/man8/burg-set-default.8*
%if %{with burgemu}
%attr(755,root,root) %{_sbindir}/burg-emu
%{_mandir}/man8/burg-emu.8*
%endif
/lib/burg-mkconfig_lib

%dir %{_libexecdir}
%config(noreplace) %verify(not md5 mtime size) %{_libexecdir}/grub.cfg
%{_libexecdir}/*.mod
%{_libexecdir}/*.lst
%ifarch %{ix86} %{x8664} sparc sparc64
%{_libexecdir}%{_libdir}.img
%{_libexecdir}/cdboot.img
%{_libexecdir}/diskboot.img
%{_libexecdir}/lnxboot.img
%{_libexecdir}/pxeboot.img
%endif

# generated by grub at runtime
%ghost %{_libexecdir}/device.map
%ghost %{_libexecdir}/core.img

%dir /lib/burg.d
%doc /lib/burg.d/README
%attr(755,root,root) /lib/burg.d/00_header
%attr(755,root,root) /lib/burg.d/10_linux
%attr(755,root,root) /lib/burg.d/30_os-prober
%attr(755,root,root) /lib/burg.d/40_custom

%dir %attr(750,root,root) %{_sysconfdir}/burg.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/burg.d/custom.cfg

%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_sbindir}/burg-mkdevicemap
%attr(755,root,root) %{_sbindir}/burg-probe
%attr(755,root,root) %{_sbindir}/burg-setup
%{_mandir}/man8/burg-mkdevicemap.8*
%{_mandir}/man8/burg-probe.8*
%{_mandir}/man8/burg-setup.8*
%endif

%{_infodir}/burg*.info*
