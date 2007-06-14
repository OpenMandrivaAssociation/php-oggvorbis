%define modname oggvorbis
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A23_%{modname}.ini

Summary:	PHP OGG wrapper for OGG/Vorbis files
Name:		php-%{modname}
Version:	0.2
Release:	%mkrel 11
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/oggvorbis
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
Patch0:		oggvorbis-0.2-label_at_end_of_compound_statement.diff
BuildRequires:	oggvorbis-devel
BuildRequires:	libogg-devel
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
fopen wrapper for OGG/Vorbis files. Decompress OGG data to PCM audio and
vice-versa.

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p0

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"

%if %mdkversion >= 200710
export CFLAGS="$CFLAGS -fstack-protector"
export CXXFLAGS="$CXXFLAGS -fstack-protector"
export FFLAGS="$FFLAGS -fstack-protector"
%endif

%{_usrsrc}/php-devel/buildext %{modname} "%{modname}.c" \
    "-logg -lvorbis -lvorbisenc -lvorbisfile" \
    "-DWITH_OGGVORBIS -DCOMPILE_DL_OGGVORBIS" \
    "-I%{_includedir}/vorbis -I%{_includedir}/ogg"

#phpize
#%%configure2_5x --with-libdir=%{_lib} \
#    --with-%{modname}=shared,%{_prefix}
#
#%%make
#mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
