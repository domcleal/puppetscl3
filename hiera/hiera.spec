%{?scl:%scl_package hiera}
%{!?scl:%global pkg_name %{name}}

%if 0%{?el5}%{?el6}
%{!?ruby_vendorlibdir: %global ruby_vendorlibdir /usr/lib/ruby/site_ruby/1.8}
%endif

#rspec seems broken(?) in epel5 and6, todo.
#rubygem(mocha) not available yet on el7.
%if 0%{?el5}%{?el6}%{?el7}
%global with_checks 0
%else
%global with_checks 1
%endif

Name:           %{?scl_prefix}hiera
Version:        1.3.1
Release:        2%{?dist}
Summary:        A simple hierarchical database supporting plugin data sources

Group:          System Environment/Base
License:        ASL 2.0
URL:            http://projects.puppetlabs.com/projects/%{name}/
Source0:        http://downloads.puppetlabs.com/hiera/%{pkg_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if 0%{?with_checks}
BuildRequires:  %{?scl_prefix}rubygem(rspec)
BuildRequires:  %{?scl_prefix}rubygem(mocha)
%endif
BuildRequires:  %{?scl_prefix_ruby}ruby-devel
%if 0%{?scl:1}
Requires:       %{?scl_prefix_ruby}ruby(release)
%else
%if 0%{?el5}%{?el6}
Requires:       %{?scl_prefix_ruby}ruby(abi) = 1.8
%else
Requires:       %{?scl_prefix_ruby}ruby(release)
%endif
%endif

%description
A simple hierarchical database supporting plugin data sources.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{ruby_vendorlibdir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_bindir}
cp -pr lib/hiera %{buildroot}%{ruby_vendorlibdir}
cp -pr lib/hiera.rb %{buildroot}%{ruby_vendorlibdir}
install -p -m0755 bin/hiera %{buildroot}%{_bindir}
install -p -m0644 ext/hiera.yaml %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_var}/lib/hiera

%check
%if 0%{?with_checks}
ruby spec/spec_helper.rb
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/hiera
%{ruby_vendorlibdir}/hiera.rb
%{ruby_vendorlibdir}/hiera
%dir %{_var}/lib/hiera
%config(noreplace) %{_sysconfdir}/hiera.yaml
%doc COPYING README.md LICENSE


%changelog
* Thu Feb 13 2014 Steve Traylen <steve.traylen@cern.ch> - 1.3.1-2
- New version 1.3.1

* Mon Sep 16 2013 Steve Traylen <steve.traylen@cern.ch> - 1.2.1-1
- New version 1.2.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 1 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-3
- Correct ruby(abi) requirement.

* Thu Sep 27 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-2
- Remove _isa tag for f18 from ruby-devel?

* Thu Sep 27 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-1
- Update to 1.0.0
- Add LICENSE file
- Add /var/lib/hiera as default data path.

* Wed May 30 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-0.2.rc3
- Update to 1.0.0rc3 and drop puppet functions.

* Wed May 16 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-0.2rc2
- Adapt to fedora guidelines.

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc2
- 1.0.0rc2 release

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc1
- 1.0.0rc1 release

* Thu May 03 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 0.3.0.28-1
- Initial Hiera Packaging. Upstream version 0.3.0.28

