# valgrind finds invalid writes in libcmocka on arm and power
# see bug #1699304 for more information
%ifarch %{arm} ppc64le
%global run_valgrind_tests OFF
%else
%global run_valgrind_tests ON
%endif

Name: libyang
Version: 2.0.112
Release: 2%{?dist}
Summary: YANG data modeling language library
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/v%{version}.tar.gz
License: BSD

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  cmake(cmocka) >= 1.0.0
BuildRequires:  make
BuildRequires:  pkgconfig(libpcre2-8) >= 10.21
BuildRequires:  valgrind

Conflicts:      %{name} < 1.0.225-3
Obsoletes:      libyang2

%package devel
Summary:    Development files for libyang
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pcre2-devel

%package devel-doc
Summary:    Documentation of libyang API
Requires:   %{name}%{?_isa} = %{version}-%{release}

%package tools
Summary:        YANG validator tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This was not properly split out before
Conflicts:      %{name} < 1.0.225-3 

%description devel
Headers of libyang library.

%description devel-doc
Documentation of libyang API.

%description tools
YANG validator tools.

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%prep
%autosetup -p1

%build
%cmake \
   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
   -DCMAKE_BUILD_TYPE:String="Package" \
   -DENABLE_LYD_PRIV=ON \
   -DENABLE_VALGRIND_TESTS=%{run_valgrind_tests}
%cmake_build

%if %fedora == 34
    %ifarch %{arm}
        pushd armv7hl-redhat-linux-gnueabi
    %else
        pushd %{_host}
    %endif
%else
    pushd redhat-linux-build
%endif
make doc
popd

%check
%if %fedora == 34
    %ifarch %{arm}
        pushd armv7hl-redhat-linux-gnueabi
    %else
        pushd %{_host}
    %endif
%else
    pushd redhat-linux-build
%endif
ctest --output-on-failure -V %{?_smp_mflags}
popd

%install
%cmake_install

mkdir -m0755 -p %{buildroot}/%{_docdir}/libyang
cp -a doc/html %{buildroot}/%{_docdir}/libyang/html

%files
%license LICENSE
%{_libdir}/libyang.so.2
%{_libdir}/libyang.so.2.*

%files tools
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz

%files devel
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/*.h
%dir %{_includedir}/libyang/

%files devel-doc
%{_docdir}/libyang

%changelog
* Wed Jan 19 2022 Tomas Korbar <tkorbar@redhat.com> - 2.0.112-2
- Fix building of libyang 2 on fedora 34

* Tue Nov 30 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.112-1
- Rebase to version 2.0.112
- Resolves: rhbz#2022586

* Mon Oct 11 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.97-1
- Rebase to version 2.0.97
- Resolves: rhbz#2012348

* Thu Sep 30 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.88-1
- Rebase to version 2.0.88
- Resolves: rhbz#2007673

* Fri Aug 06 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.7-1
- Rebase to version 2.0.7
- Resolves: rhbz#1959645

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.225-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

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
