#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Intel(R) PRO/Wireless 2200 Driver for Linux
Summary(pl):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 2200
Name:		ipw2200
Version:	0.22
%define		_rel	1
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw2200/%{name}-%{version}.tgz
# Source0-md5:	d8d12c5b47611552c3c90750814116ba
URL:		http://ipw2200.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	sed >= 4.0
Requires:	ipw2200-firmware >= 2.2
ExclusiveArch:	%{ix86} amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2200/2915 Network Connection mini PCI adapter.

%description -l pl
Ten projekt zosta³ stworzony przez Intela, aby umo¿liwiæ obs³ugê kart
mini PCI Intel PRO/Wireless 2200/2915 Network Connection.

%package -n kernel-net-ipw2200
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 2200
Summary(pl):	Modu³ j±dra Linuksa dla kart Intel(R) PRO/Wireless 2200
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	ipw2200-firmware >= 2.2
Requires:	hotplug
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-ipw2200
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 2200 and 2915.

%description -n kernel-net-ipw2200 -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa dla kart Intel(R)
PRO/Wireless 2200 oraz 2915.

%package -n kernel-smp-net-ipw2200
Summary:	Linux SMP kernel module for the Intel(R) PRO/Wireless 2200
Summary(pl):	Modu³ j±dra Linuksa SMP dla kart Intel(R) PRO/Wireless 2200
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
PreReq:		kernel-net-hostap = 0.1.3
Requires:	ipw2200-firmware >= 2.2
Requires:	hotplug
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-ipw2200
This package contains Linux SMP kernel drivers for the Intel(R)
PRO/Wireless 2200 and 2915.

%description -n kernel-smp-net-ipw2200 -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa SMP dla kart Intel(R)
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
    touch include/config/MARKER
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
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ieee80211*.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ipw2200.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-ipw2200
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/ieee80211*.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/ipw2200.ko*
%endif
