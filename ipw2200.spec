#
# TODO:	- build still depends on ieee80211-devel and kernel*-headers
#	  installation order on builder machine.
#	- there is a problem with unloading of ipw2200 module
#	  IMHO we should make subpackage of the vanilla ipw2200
#	  driver, rename this package to ipw2200_current (but not 
#	  the contents of it) and add obsoletes to the both. 
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
%define		_ieeever	1.2.17
%define		_fwver	3.0
%define		_mod_suffix	current
Summary:	Intel(R) PRO/Wireless 2200 Driver for Linux
Summary(de.UTF-8):	Intel(R) PRO/Wireless 2200 Treiber für Linux
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 2200
Name:		ipw2200
Version:	1.2.2
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw2200/%{name}-%{version}.tgz
# Source0-md5:	570959316e56765716824b89adf88d31
Patch0:		%{name}-monitor.patch
Patch1:		%{name}-1.2.0-config.patch
URL:		http://ipw2200.sourceforge.net/
BuildRequires:	ieee80211-devel >= %{_ieeever}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires:	ipw2200-firmware = %{_fwver}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2200/2915 Network Connection mini PCI adapter.

%description -l de.UTF-8
Dieses Projekt wurde von Intel gestartet um die Wartung von mini PCI
Intel PRO/Wireless 2200/2915 Netzwerkkarten zu ermöglichen.

%description -l pl.UTF-8
Ten projekt został stworzony przez Intela, aby umożliwić obsługę kart
mini PCI Intel PRO/Wireless 2200/2915 Network Connection.

%package -n kernel%{_alt_kernel}-net-%{name}
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 2200
Summary(de.UTF-8):	Linux Kernel Modul für Intel(R) PRo/Wireless 2200 Netzwerkkarten
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart Intel(R) PRO/Wireless 2200
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	ipw2200-firmware = %{_fwver}
%(rpm -q --qf 'Requires: kernel%{_alt_kernel}-net-ieee80211 = %%{epoch}:%%{version}-%%{release}\n' ieee80211-devel | sed -e 's/ (none):/ /' | grep -v "is not")
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-net-%{name}
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 2200 and 2915.

%description -n kernel%{_alt_kernel}-net-%{name} -l de.UTF-8
Dieses Paket enthält Linux Kernel Treiber für Intel(R) PRO/Wireless
2200 und 2915 Netzwerkkarten.

%description -n kernel%{_alt_kernel}-net-%{name} -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa dla kart Intel(R)
PRO/Wireless 2200 oraz 2915.

%prep
%setup -q
%patch0 -p1
%if %{with dist_kernel}
%patch1 -p1
%endif

%build
%build_kernel_modules -m ipw2200

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -s %{_mod_suffix} -n %{name} -m ipw2200 -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{name}
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ipw2200-%{_mod_suffix}.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{name}.conf
