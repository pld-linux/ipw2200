#
# TODO:
# - fix the include dir in kernel-net-ieee80211 and change IEEE80211_INC here (l. 93)
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Intel(R) PRO/Wireless 2200 Driver for Linux
Summary(pl):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 2200
Name:		ipw2200
Version:	1.0.6
%define		_rel	2
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw2200/%{name}-%{version}.tgz
# Source0-md5:	d49f301ce8cffbd1cfbdb51061df3ac8
URL:		http://ipw2200.sourceforge.net/
BuildRequires:	ieee80211-devel
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	sed >= 4.0
Requires:	ipw2200-firmware = 2.3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2200/2915 Network Connection mini PCI adapter.

%description -l pl
Ten projekt zosta� stworzony przez Intela, aby umo�liwi� obs�ug� kart
mini PCI Intel PRO/Wireless 2200/2915 Network Connection.

%package -n kernel-net-ipw2200
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 2200
Summary(pl):	Modu� j�dra Linuksa dla kart Intel(R) PRO/Wireless 2200
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	ipw2200-firmware = 2.3
Requires:	kernel-net-ieee80211
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-ipw2200
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 2200 and 2915.

%description -n kernel-net-ipw2200 -l pl
Ten pakiet zawiera sterowniki j�dra Linuksa dla kart Intel(R)
PRO/Wireless 2200 oraz 2915.

%package -n kernel-smp-net-ipw2200
Summary:	Linux SMP kernel module for the Intel(R) PRO/Wireless 2200
Summary(pl):	Modu� j�dra Linuksa SMP dla kart Intel(R) PRO/Wireless 2200
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	ipw2200-firmware = 2.3
Requires:	kernel-smp-net-ieee80211
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-ipw2200
This package contains Linux SMP kernel drivers for the Intel(R)
PRO/Wireless 2200 and 2915.

%description -n kernel-smp-net-ipw2200 -l pl
Ten pakiet zawiera sterowniki j�dra Linuksa SMP dla kart Intel(R)
PRO/Wireless 2200 oraz 2915.

%prep
%setup -q
#sed -i 's:CONFIG_IPW_DEBUG=y::' Makefile

%build
# kernel module(s)
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	%if %{without dist_kernel}
                ln -sf %{_kernelsrcdir}/scripts
        %endif
	touch include/config/MARKER
	export IEEE80211_INC=%{_kernelsrcdir}/include
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv *.ko built/$cfg
done

%install
rm -rf $RPM_BUILD_ROOT


cd built
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless
%if %{with smp} && %{with dist_kernel}
install smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-ipw2200
%depmod %{_kernel_ver}

%postun	-n kernel-net-ipw2200
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-ipw2200
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-net-ipw2200
%depmod %{_kernel_ver}smp

%files -n kernel-net-ipw2200
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ipw2200.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-ipw2200
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/ipw2200.ko*
%endif
