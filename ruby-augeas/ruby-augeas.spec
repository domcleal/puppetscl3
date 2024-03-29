%{?scl:%scl_package ruby-augeas}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}ruby-augeas
Version:        0.5.0
Release:        2%{?dist}
Summary:        Ruby bindings for Augeas
Group:          Development/Languages

License:        LGPLv2+
URL:            http://augeas.net
Source0:        http://download.augeas.net/ruby/ruby-augeas-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{?scl_prefix_ruby}ruby %{?scl_prefix_ruby}rubygem(rake) %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires:  %{?scl_prefix_ruby}ruby-devel
BuildRequires:  augeas-devel >= 1.0.0
BuildRequires:  pkgconfig
Requires:       %{?scl_prefix_ruby}ruby(release)
Requires:       augeas-libs >= 1.0.0
Provides:       %{?scl_prefix}ruby(augeas) = %{version}

%description
Ruby bindings for augeas.

%prep
%setup -q -n %{pkg_name}-%{version}


%build
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
%{?scl:scl enable %{scl} "}
rake build
%{?scl:"}

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{ruby_vendorlibdir}
install -d -m0755 %{buildroot}%{ruby_vendorarchdir}
install -p -m0644 lib/augeas.rb %{buildroot}%{ruby_vendorlibdir}
install -p -m0755 ext/augeas/_augeas.so %{buildroot}%{ruby_vendorarchdir}

%check
%{?scl:scl enable %{scl} "}
testrb tests/tc_augeas.rb
%{?scl:"}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README.rdoc NEWS
%{ruby_vendorlibdir}/augeas.rb
%{ruby_vendorarchdir}/_augeas.so


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 David Lutterkort <lutter@redhat.com> - 0.5.0-1
- New version; updated spec file for latest guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 David Lutterkort <lutter@redhat.com> - 0.4.1-1
- New version

* Tue Mar 29 2011 David Lutterkort <lutter@redhat.com> - 0.4.0-1
- Require augeas-0.8.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 12 2009 David Lutterkort <lutter@redhat.com> - 0.3.0-1
- New version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 David Lutterkort <dlutter@redhat.com> - 0.2.0-1
- New version

* Fri May  9 2008 David Lutterkort <dlutter@redhat.com> - 0.1.0-1
- Fixed up in accordance with Fedora guidelines

* Mon Mar 3 2008 Bryan Kearney <bkearney@redhat.com> - 0.0.1-1
- Initial specfile
