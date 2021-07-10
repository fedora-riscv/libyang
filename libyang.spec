# valgrind finds invalid writes in libcmocka on arm and power
# see bug #1699304 for more information
%ifarch %{arm} ppc64le
%global run_valgrind_tests OFF
%else
%global run_valgrind_tests ON
%endif

# Use arch-independent builddir
%global _vpath_builddir %{_vendor}-%{_target_os}-build

# library soname major version
%global somajor 1

Name:           libyang
Version:        1.0.225
Release:        3%{?dist}
Summary:        YANG data modeling language library
License:        BSD
URL:            https://github.com/CESNET/libyang
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  libcmocka-devel
BuildRequires:  make
BuildRequires:  pcre-devel
BuildRequires:  python3-devel
BuildRequires:  swig >= 3.0.12
BuildRequires:  valgrind

# This was not properly split out before
Conflicts:      %{name} < 1.0.225-3

%package tools
Summary:        YANG validator tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This was not properly split out before
Conflicts:      %{name} < 1.0.225-3

%package devel
Summary:        Development files for libyang
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pcre-devel

%package devel-doc
Summary:        Documentation of libyang API
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%package cpp
Summary:        C++ bindings for libyang
Requires:       %{name}%{?_isa} = %{version}-%{release}

%package cpp-devel
Summary:        Development files for libyang-cpp
Requires:       %{name}-cpp%{?_isa} = %{version}-%{release}
Requires:       pcre-devel

%package -n python3-libyang
Summary:        Python3 bindings for libyang
Requires:       %{name}-cpp%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-libyang}

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%description tools
YANG validator tools.

%description devel
Headers of libyang library.

%description devel-doc
Documentation of libyang API.

%description cpp
Bindings of libyang library to C++ language.

%description cpp-devel
Headers of bindings to c++ language.

%description -n python3-libyang
Bindings of libyang library to python language.

%prep
%autosetup -p1

%build
%cmake \
   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
   -DCMAKE_BUILD_TYPE:String="Package" \
   -DENABLE_LYD_PRIV=ON \
   -DGEN_JAVA_BINDINGS=OFF \
   -DGEN_JAVASCRIPT_BINDINGS=OFF \
   -DGEN_LANGUAGE_BINDINGS=ON \
   -DENABLE_VALGRIND_TESTS=%{run_valgrind_tests}

%cmake_build

# Build documentation
%cmake_build --target doc

%check
%ctest

%install
%cmake_install

mkdir -m0755 -p %{buildroot}/%{_docdir}/libyang
cp -a doc/html %{buildroot}/%{_docdir}/libyang/html

%files
%license LICENSE
%{_libdir}/libyang.so.%{somajor}{,.*}
%{_libdir}/libyang%{somajor}/

%files tools
%{_bindir}/yanglint
%{_bindir}/yangre
%{_mandir}/man1/yanglint.1*
%{_mandir}/man1/yangre.1*

%files devel
%dir %{_includedir}/libyang/
%{_includedir}/libyang/*.h
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc

%files devel-doc
%{_docdir}/libyang/

%files cpp
%{_libdir}/libyang-cpp.so.%{somajor}{,.*}

%files cpp-devel
%dir %{_includedir}/libyang/
%{_includedir}/libyang/*.hpp
%{_libdir}/libyang-cpp.so
%{_libdir}/pkgconfig/libyang-cpp.pc

%files -n python3-libyang
%{python3_sitearch}/yang.py
%{python3_sitearch}/_yang.so
%{python3_sitearch}/__pycache__/yang*

%changelog
* Sat Jul 10 2021 Neal Gompa <ngompa@datto.com> - 1.0.225-3
- Clean up the spec file for legibility and modern spec standards
- Split out tools into their own subpackage
- Remove archfulness from the build path to fix documentation build

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.225-2
- Rebuilt for Python 3.10

* Tue Mar 09 2021 Tomas Korbar <tkorbar@redhat.com> - 1.0.225-1
- Rebase to version 1.0.225
- Resolves: rhbz#1936718

* Wed Feb 03 2021 Tomas Korbar <tkorbar@redhat.com> - 1.0.215-1
- Rebase to version 1.0.215
- Resolves: rhbz#1921779

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.184-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 02 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.0.184-3
- Fix FTBFS by disabling valgrind on power since it finds bogus invalid
  writes in libcmocka

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.184-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.184-1
- Update to 1.0.184
- Fix build

* Fri Jun 19 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.176-1
- Update to 1.0.176

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.167-2
- Rebuilt for Python 3.9

* Mon May 18 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.167-1
- Update to 1.0.167

* Fri Feb 07 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.130-1
- Rebase to version 1.0.130 (#1797495)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Tomas Korbar <tkorbar@redhat.com> - 1.0.101-1
- Rebase to version 1.0.101
- Fix CVE-2019-19333 (#1780495)
- Fix CVE-2019-19334 (#1780494)

* Fri Oct 25 2019 Tomas Korbar <tkorbar@redhat.com> - 1.0.73-1
- Rebase to version 1.0.73 (#1758512)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.105-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.105-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Initial import (#1699846).

* Fri Apr 26 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Change specfile accordingly to mosvald's review
- Remove obsolete ldconfig scriptlets
- libyang-devel-doc changed to noarch package
- Add python_provide macro to python3-libyang subpackage
- Remove obsolete Requires from libyang-cpp-devel
- Start using cmake with smp_mflags macro

* Wed Apr 03 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Initial commit of package after editation of specfile
