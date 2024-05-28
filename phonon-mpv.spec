%bcond_with qt4
%bcond_without qt5
%bcond_without qt6

%define git 20240528

Summary:	Phonon MPV Backend
Name:		phonon-mpv
Version:	0.0.8
Release:	%{?git:0.%{git}.}1
License:	GPLv2+
Group:		Video
Url:		https://github.com/OpenProgger/phonon-mpv
%if 0%{?git:1}
Source0:	https://github.com/OpenProgger/phonon-mpv/archive/refs/heads/master.tar.gz#/phonon-mpv-%{git}.tar.gz
%else
Source0:	http://download.kde.org/stable/phonon/phonon-backend-mpv/%{version}/phonon-backend-mpv-%{version}.tar.xz
%endif
%if %{with qt4}
BuildRequires:	automoc4
BuildRequires:	pkgconfig(phonon)
%endif
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(mpv)
%if %{with qt5}
BuildRequires:	pkgconfig(phonon4qt5)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5X11Extras)
%endif
%if %{with qt6}
BuildRequires:	pkgconfig(phonon4qt6)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6CoreTools)
BuildRequires:	cmake(Qt6GuiTools)
BuildRequires:	cmake(Qt6DBusTools)
BuildRequires:	cmake(Qt6WidgetsTools)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
%endif
Provides:	phonon-backend
Suggests:	%{name}-translations

%description
This package allows Phonon (the KDE media library) to use MPV for audio and
video playback.

%if 0
%package translations
Summary:	Translations for the phonon MPV backends (common to all Qt versions)
Group:		Video
BuildArch:	noarch

%description translations
Translations for the phonon MPV backends (common to all Qt versions)

%files translations -f %{name}.lang
%endif

%if %{with qt4}
%files
%{_libdir}/kde4/plugins/phonon_backend/phonon_mpv.so
%{_datadir}/kde4/services/phononbackends/mpv.desktop
%endif

%package -n phonon4qt5-mpv
Summary:	Phonon MPV Backend
Provides:	phonon4qt5-backend
Requires:	mpv
Suggests:	%{name}-translations

%description -n phonon4qt5-mpv
Phonon4Qt5 MPV Backend.

%files -n phonon4qt5-mpv
%{_libdir}/qt5/plugins/phonon4qt5_backend/phonon_mpv_qt5.so

%package -n phonon4qt6-mpv
Summary:	Phonon MPV Backend
Provides:	phonon4qt6-backend
Requires:	mpv
Suggests:	%{name}-translations

%description -n phonon4qt6-mpv
Phonon4Qt6 MPV Backend.

%files -n phonon4qt6-mpv
%{_qtdir}/plugins/phonon4qt6_backend/phonon_mpv_qt6.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n phonon%{!?git:-backend}-mpv-%{?git:master}%{!?git:%{version}}
%if %{with qt4}
export CMAKE_BUILD_DIR=build-qt4
%cmake -DPHONON_BUILD_PHONON4QT5:BOOL=OFF \
	-DQT_QMAKE_EXECUTABLE=%{_prefix}/lib/qt4/bin/qmake \
	-G Ninja
cd ..
%endif

%if %{with qt5}
# The cmake_kde5 macro doesn't currently respect CMAKE_BUILD_DIR,
# so let's make sure the Qt5 build uses the default name
export CMAKE_BUILD_DIR=build
%cmake_kde5 -DPHONON_BUILD_PHONON4QT5:BOOL=ON \
	-DPHONON_BUILD_QT5:BOOL=ON \
	-DPHONON_BUILD_QT6:BOOL=OFF \
	-DQT_QMAKE_EXECUTABLE=%{_libdir}/qt5/bin/qmake
cd ..
%endif

%if %{with qt6}
export CMAKE_BUILD_DIR=build-qt6
%cmake -DQT_MAJOR_VERSION=6 \
	-DPHONON_BUILD_QT5:BOOL=OFF \
	-DPHONON_BUILD_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja
cd ..
%endif

%build
%if %{with qt4}
%ninja_build -C build-qt4
%endif

%if %{with qt5}
%ninja_build -C build
%endif

%if %{with qt6}
%ninja_build -C build-qt6
%endif

%install
%if %{with qt4}
%ninja_install -C build-qt4
%endif

%if %{with qt5}
%ninja_install -C build
%endif

%if %{with qt6}
%ninja_install -C build-qt6
%endif

find %{buildroot}%{_datadir}/locale -name "*.qm" |while read r; do
	L=`echo $r |rev |cut -d/ -f3 |rev`
	echo "%%lang($L) %%{_datadir}/locale/$L/LC_MESSAGES/*.qm" >>%{name}.lang
done
