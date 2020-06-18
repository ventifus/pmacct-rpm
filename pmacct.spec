Name:           pmacct
Version:        1.7.5
Release:        1%{?dist}
Summary:        Accounting and aggregation toolsuite for IPv4 and IPv6
License:        GPLv2+
URL:            http://www.pmacct.net/
Source0:        http://www.pmacct.net/pmacct-%{version}.tar.gz
Source1:        nfacctd.service
Source2:        nfacctd
Source3:        pmacctd.service
Source4:        pmacctd
Source5:        sfacctd.service
Source6:        sfacctd

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  mariadb-devel
BuildRequires:  libpcap-devel
BuildRequires:  libstdc++-static
BuildRequires:  pkgconfig
BuildRequires:  postgresql-devel
BuildRequires:  sqlite-devel >= 3.0.0
BuildRequires:  pkgconfig(geoip)
BuildRequires:  pkgconfig(jansson)
BuildRequires:  systemd

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
pmacct is a small set of passive network monitoring tools to measure, account,
classify and aggregate IPv4 and IPv6 traffic; a pluggable and flexible
architecture allows to store the collected traffic data into memory tables or
SQL (MySQL, SQLite, PostgreSQL) databases. pmacct supports fully customizable
historical data breakdown, flow sampling, filtering and tagging, recovery
actions, and triggers. Libpcap, sFlow v2/v4/v5 and NetFlow v1/v5/v7/v8/v9 are
supported, both unicast and multicast. Also, a client program makes it easy to
export data to tools like RRDtool, GNUPlot, Net-SNMP, MRTG, and Cacti.

%prep
%autosetup

# fix permissions
chmod -x sql/pmacct-*

%build
export CFLAGS="%{optflags} -Wno-return-type"
%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --sbindir=%{_sbindir} \
    --enable-l2 \
    --enable-mysql \
    --enable-pgsql \
    --enable-sqlite3 \
    --enable-geoip \
    --enable-jansson

%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install

# install sample configuration files
install -Dp examples/nfacctd-sql.conf.example %{buildroot}/%{_sysconfdir}/%{name}/nfacctd.conf
install -Dp examples/pmacctd-sql.conf.example %{buildroot}/%{_sysconfdir}/%{name}/pmacctd.conf

# install systemd units
install -d %{buildroot}/%{_unitdir} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install %{SOURCE1} %{SOURCE3} %{SOURCE5} %{buildroot}/%{_unitdir}
install %{SOURCE2} %{SOURCE4} %{SOURCE6} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

%post
%systemd_post nfacctd.service
%systemd_post pmacctd.service
%systemd_post sfacctd.service

%preun
%systemd_preun nfacctd.service
%systemd_preun pmacctd.service
%systemd_preun sfacctd.service

%postun
%systemd_postun_with_restart nfacctd.service
%systemd_postun_with_restart pmacctd.service
%systemd_postun_with_restart sfacctd.service

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS ChangeLog CONFIG-KEYS FAQS QUICKSTART UPGRADE
%doc docs examples sql
%{_bindir}/pmacct
#
%{_sbindir}/nfacctd
%{_sbindir}/pmacctd
%{_sbindir}/pmbgpd
%{_sbindir}/pmbmpd
%{_sbindir}/pmtelemetryd
%{_sbindir}/sfacctd
#
%{_unitdir}/nfacctd.service
%{_unitdir}/pmacctd.service
%{_unitdir}/sfacctd.service
#
%{_sysconfdir}/sysconfig/%{name}/nfacctd
%{_sysconfdir}/sysconfig/%{name}/pmacctd
%{_sysconfdir}/sysconfig/%{name}/sfacctd
#
%dir %{_sysconfdir}/pmacct
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/nfacctd.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/pmacctd.conf

%{_libdir}/pmacct/examples/custom/libcustom.la
%{_libdir}/pmacct/examples/lg/pmbgp
%{_prefix}/share/pmacct/*
%{_prefix}/share/pmacct/docs/*
%{_prefix}/share/pmacct/examples/*
%{_prefix}/share/pmacct/sql/*

%changelog
* Mon Dec 21 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.5.2-2
- Enable ULOG

* Sun Dec 13 2015 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 1.5.2-1
- Initial packaging based on OpenSUSE rpms packaged by Peter Nixon and available
  at http://download.opensuse.org/repositories/server:/monitoring/

