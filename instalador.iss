; Instalador para Windows (Inno Setup). Lo compila GitHub Actions:
;   iscc /DVersion=1.3 instalador.iss   (después de pyinstaller --onedir)
; Se instala solo para el usuario, sin pedir permisos de administrador. El
; acceso directo abre el juego en la consola clásica (conhost), donde el juego
; puede ajustar la fuente y los colores; Windows Terminal no lo permite.

#ifndef Version
  #define Version "0.0"
#endif

[Setup]
AppId={{8DC90A69-C885-5F0F-BD64-5163E1ABC96B}
AppName=Aminomon
AppVersion={#Version}
AppPublisher=leomorgzzz
AppPublisherURL=https://github.com/leomorgzzz/aminomon
DefaultDirName={autopf}\Aminomon
DefaultGroupName=Aminomon
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=.
OutputBaseFilename=Aminomon-Instalador-Windows
SetupIconFile=icono.ico
UninstallDisplayIcon={app}\Aminomon.exe
WizardStyle=modern
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "escritorio"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\Aminomon\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{autoprograms}\Aminomon"; Filename: "{sys}\conhost.exe"; Parameters: """{app}\Aminomon.exe"""; WorkingDir: "{app}"; IconFilename: "{app}\Aminomon.exe"
Name: "{autodesktop}\Aminomon"; Filename: "{sys}\conhost.exe"; Parameters: """{app}\Aminomon.exe"""; WorkingDir: "{app}"; IconFilename: "{app}\Aminomon.exe"; Tasks: escritorio

[Run]
Filename: "{sys}\conhost.exe"; Parameters: """{app}\Aminomon.exe"""; WorkingDir: "{app}"; Description: "{cm:LaunchProgram,Aminomon}"; Flags: nowait postinstall skipifsilent
