%global gem_name rgen
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%{!?enable_test: %global enable_test 0}

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.6.6
Release: 2%{?dist}
Summary: Ruby Modelling and Generator Framework
Group: Development/Languages
License: MIT
URL: https://github.com/mthiede/rgen
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby(release)

BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%if 0%{enable_test} > 0
BuildRequires: %{?scl_prefix}rubygem(nokogiri)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
%endif

BuildArch: noarch

Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
RGen is a framework for Model Driven Software Development (MDSD) in Ruby. This
means that it helps you build Metamodels, instantiate Models, modify and
transform Models and finally generate arbitrary textual content from it.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%if 0%{enable_test} > 0
%check
%{?scl:scl enable %{scl} "}
RUBYOPT=-rubygems ruby test/rgen_test.rb
%{?scl:"}
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/test
%{gem_instdir}/Rakefile

%changelog
* Wed Jan 22 2014 Sam Kottler <shk@redhat.com> - 0.6.6-2
- Fixes based on review feedback

* Mon Jan 06 2014 Sam Kottler <shk@redhat.com> - 0.6.6-1
- Initial package
