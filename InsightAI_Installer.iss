#define MyAppName "InsightAI Offline"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "InsightAI"
#define MyAppExeName "InsightAI Offline.exe"

[Setup]
AppId={{8F6E7E5A-2B42-4A6D-9A4E-123456789ABC}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\InsightAI Offline
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=InsightAI_Offline_Setup

Compression=lzma
SolidCompression=yes

ArchitecturesInstallIn64BitMode=x64

SetupIconFile=assets\insightai.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

PrivilegesRequired=admin

[Files]
Source: "dist\InsightAI Offline\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent