Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strDir = fso.GetParentFolderName(WScript.ScriptFullName)
strExe = fso.BuildPath(strDir, "dist\NETSCAN_CCTV.exe")
strApp = fso.BuildPath(strDir, "app.py")
strPy = WshShell.ExpandEnvironmentStrings("%LocalAppData%\Programs\Python\Python313\pythonw.exe")

If fso.FileExists(strExe) Then
    WshShell.CurrentDirectory = strDir
    WshShell.Run """" & strExe & """", 0, False
Else
    If Not fso.FileExists(strPy) Then
        strPy = "pythonw"
    End If
    WshShell.CurrentDirectory = strDir
    WshShell.Run """" & strPy & """ """ & strApp & """", 0, False
End If
