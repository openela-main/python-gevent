%global __provides_exclude_from ^%{python2_sitearch}/.*\\.so$ ^%{python3_sitearch}/.*\\.so$
%global modname gevent
%global optflags %(echo %{optflags} -I%{_includedir}/libev)

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:          python-%{modname}
Version:       1.2.2
Release:       4%{?dist}
Summary:       A coroutine-based Python networking library

License:       MIT
URL:           http://www.gevent.org/
Source0:       https://files.pythonhosted.org/packages/source/g/%{modname}/%{modname}-%{version}.tar.gz

# https://github.com/gevent/gevent/pull/979
Patch1:        0001-always-obey-GEVENT_NO_CFFI_BUILD.patch

BuildRequires: c-ares-devel
BuildRequires: libev-devel

%description
gevent is a coroutine-based Python networking library that uses greenlet to
provide a high-level synchronous API on top of libevent event loop.

Features include:

  * convenient API around greenlets
  * familiar synchronization primitives (gevent.event, gevent.queue)
  * socket module that cooperates
  * WSGI server on top of libevent-http
  * DNS requests done through libevent-dns
  * monkey patching utility to get pure Python modules to cooperate

%if %{with python2}
%package -n python2-%{modname}
Summary:       %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires: python2-devel
Requires:      python2-greenlet

%description -n python2-%{modname}
gevent is a coroutine-based Python networking library that uses greenlet to
provide a high-level synchronous API on top of libevent event loop.

Features include:

  * convenient API around greenlets
  * familiar synchronization primitives (gevent.event, gevent.queue)
  * socket module that cooperates
  * WSGI server on top of libevent-http
  * DNS requests done through libevent-dns
  * monkey patching utility to get pure Python modules to cooperate

Python 2 version.
%endif # with python2

%package -n python3-%{modname}
Summary:       %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires: python3-devel
Requires:      python3-greenlet

%description -n python3-%{modname}
gevent is a coroutine-based Python networking library that uses greenlet to
provide a high-level synchronous API on top of libevent event loop.

Features include:

  * convenient API around greenlets
  * familiar synchronization primitives (gevent.event, gevent.queue)
  * socket module that cooperates
  * WSGI server on top of libevent-http
  * DNS requests done through libevent-dns
  * monkey patching utility to get pure Python modules to cooperate

Python 3 version.

%prep
%autosetup -n %{modname}-%{version}
# Remove bundled libraries
rm -r deps
# Upstream intentionally includes C extension sources in the built package, 
# because... reasons (PyPy I think?) however we do not want that. Sources will 
# go into debuginfo as normal.
sed -i -e 's/include_package_data=True/include_package_data=False/' setup.py

%build
export LIBEV_EMBED=0
export CARES_EMBED=0
export GEVENT_NO_CFFI_BUILD=1
%if %{with python2}
rm src/gevent/_*3.py*
%py2_build
%endif # with python2
rm src/gevent/_*2.py
%py3_build

%install
export LIBEV_EMBED=0
export CARES_EMBED=0
export GEVENT_NO_CFFI_BUILD=1
%if %{with python2}
%py2_install
%endif # with python2
%py3_install
find %{buildroot} -name '.buildinfo' -delete
# Correct the permissions.
find %{buildroot} -name '*.so' -exec chmod 755 {} ';'

%if %{with python2}
%files -n python2-%{modname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/%{modname}*
%endif # with python2

%files -n python3-%{modname}
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{modname}*

%changelog
* Mon Apr 29 2019 Brian C. Lane <bcl@redhat.com> - 1.2.2-4
- Remove the python2 files before running py3_install
  Resolves: rhbz#1704111

* Wed Jul 18 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.2.2-3
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 09 2017 Dan Callaghan <dcallagh@redhat.com> - 1.2.2-1
- Update to 1.2.2 (RHBZ#1389634)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.2-2
- Rebuild for Python 3.6

* Sun Jul 24 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.2-1
- Update to 1.1.2 (RHBZ #1359455)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr 05 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.1-1
- Update to 1.1.1 (RHBZ #1323855)

* Tue Mar 15 2016 Dan Callaghan <dcallagh@redhat.com> - 1.1.0-1
- Update to 1.1.0 final release

* Wed Feb 17 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1-0.8.rc4
- Update to 1.1rc4 (RHBZ #1309141)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-0.7.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Dan Callaghan <dcallagh@redhat.com> - 1.1-0.6.rc3
- Update to 1.1rc3

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.5.b6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 24 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1-0.4.b6
- Fix description in spec

* Sun Oct 18 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1-0.3.b6
- Update to 1.1b6 (RHBZ #1272717)

* Tue Oct 06 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1-0.2.b5
- Drop use of unneeded %%{py3dir}

* Mon Oct 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1-0.1.b5
- Update to 1.1b5 (RHBZ #1244452)
- Add python3 support
- Follow modern RPM packaging guidelines

* Fri Jun 26 2015 Dan Callaghan <dcallagh@redhat.com> - 1.0.2-2
- removed version requirement for greenlet

* Mon Jun 22 2015 Dan Callaghan <dcallagh@redhat.com> - 1.0.2-1
- bug fix release 1.0.2:
  https://github.com/gevent/gevent/blob/v1.0.2/changelog.rst#release-102-may-23-2015

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-1
- Update to 1.0.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Orion Poplawski <orion@cora.nwra.com> - 1.0-1
- Update to 1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Silas Sewell <silas@sewell.org> - 0.13.8-1
- Update to 0.13.8

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 0.13.6-1
- Update to 0.13.6

* Wed Feb 16 2011 Silas Sewell <silas@sewell.ch> - 0.13.3-1
- Update to 0.13.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 09 2010 Silas Sewell <silas@sewell.ch> - 0.13.1-1
- Update to 0.13.1

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Silas Sewell <silas@sewell.ch> - 0.13.0-1
- Update to 0.13.0

* Fri Apr 23 2010 Silas Sewell <silas@sewell.ch> - 0.12.2-2
- Remove setuptools requirement

* Wed Mar 17 2010 Silas Sewell <silas@sewell.ch> - 0.12.2-1
- Initial build
