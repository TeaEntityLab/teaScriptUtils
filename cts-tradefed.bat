set SDK_ROOT=%ANDROID_HOME%
path=%path%;%SDK_ROOT%\platform-tools
set CTS_ROOT=C:\
set JAR_HOME=%CTS_ROOT%\android-cts\tools
set JAR_PATH=%JAR_HOME%\ddmlib-prebuilt.jar;%JAR_HOME%\tradefed-prebuilt.jar;%JAR_HOME%\hosttestlib.jar;%JAR_HOME%\cts-tradefed.jar

java -Xmx512M -cp %JAR_PATH% -DCTS_ROOT=%CTS_ROOT% com.android.cts.tradefed.command.CtsConsole %*