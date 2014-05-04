%global scl_name_base puppetscl
%global scl_name_version 3
%global scl %{scl_name_base}%{scl_name_version}
%scl_package %scl

# Fallback to ruby200
%{!?scl_ruby:%global scl_ruby ruby200}
%{!?scl_prefix_ruby:%global scl_prefix_ruby %{scl_ruby}-}

# Do not produce empty debuginfo package.
%global debug_package %{nil}

%global install_scl 1

Summary: Package that installs %scl
Name: %scl_name
Version: 1.0
Release: 1%{?dist}
License: GPLv2+
Source0: README
Source1: LICENSE
# This should be removed as soon as scl-utils automatically generate
# dependencies on scl -runtime (rhbz#1054711).
Source2: puppetscl3.attr
%if 0%{?install_scl}
Requires: ruby200
%endif
BuildRequires: help2man
BuildRequires: scl-utils-build
BuildRequires: %{scl_prefix_ruby}scldevel
BuildRequires: %{scl_prefix_ruby}rubygems-devel

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils
Requires: %{scl_prefix_ruby}runtime
Requires: %{_root_bindir}/scl_source

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build
Requires: %{scl_runtime}
Requires: %{scl_prefix_ruby}scldevel

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl
Provides: scldevel(%{scl_name_base})

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -T -c

# Expand macros used in README file.
cat > README << EOF
%{expand:%(cat %{SOURCE0})}
EOF

cp %{SOURCE1} .

%build
# Generate a helper script that will be used by help2man.
cat > h2m_help << 'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_help

# Generate the man page from include.h2m and ./h2m_help --help output.
help2man -N --section 7 ./h2m_help -o %{scl_name}.7

%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
export GEM_PATH=%{gem_dir}:\${GEM_PATH:+\${GEM_PATH}}\${GEM_PATH:-\`scl enable %{scl_ruby} -- ruby -e "print Gem.path.join(':')"\`}

. scl_source enable %{scl_ruby}
EOF

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Install generated man page.
mkdir -p %{buildroot}%{_mandir}/man7/
install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs/
cp %{SOURCE2} %{buildroot}%{_rpmconfigdir}/fileattrs/


scl enable %{scl_ruby} - << \EOF
# Fake puppetscl3 SCL environment.
# TODO: Is there a way how to leverage the enable scriptlet created above?
GEM_PATH=%{gem_dir}:${GEM_PATH:+${GEM_PATH}}${GEM_PATH:-`ruby -e "print Gem.path.join(':')"`} \
X_SCLS=puppetscl3 \
ruby -rfileutils > rubygems_filesystem.list << \EOR
  # Create RubyGems filesystem.
  Gem.ensure_gem_subdirectories '%{buildroot}%{gem_dir}'
  FileUtils.mkdir_p File.join '%{buildroot}', Gem.default_ext_dir_for('%{gem_dir}')

  # Output the relevant directories.
  Gem.default_dirs[:%{scl}_system].each { |k, p| puts p }
EOR
EOF

%files

%files runtime -f rubygems_filesystem.list
%doc README LICENSE
%scl_files
# Own the manual directories (rhbz#1080036, rhbz#1072319).
%dir %{_mandir}/man1
%dir %{_mandir}/man5
%dir %{_mandir}/man7
%{_mandir}/man7/%{scl_name}.*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config
%{_rpmconfigdir}/fileattrs

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Sun May 04 2014 Dominic Cleal <dcleal@redhat.com> 1.0-1
- new package built with tito

* Wed Apr 02 2014 Dominic Cleal <dcleal@redhat.com> - 1-1
- Initial package.
