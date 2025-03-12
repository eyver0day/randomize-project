[Setup]
AppName=Randomize
AppVersion=1.0
DefaultDirName={pf}\Randomize
DefaultGroupName=Randomize
OutputBaseFilename=RandomizeInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\randomize.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Randomize"; Filename: "{app}\randomize.exe"
Name: "{group}\Desinstalar Randomize"; Filename: "{uninstallexe}"
