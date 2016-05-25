set SDK_ROOT=%ANDROID_HOME%
path=%path%;%SDK_ROOT%\platform-tools
set XTS_ROOT=D:\
set JAR_HOME=%XTS_ROOT%\android-xts\tools
set JAR_PATH=%JAR_HOME%\xts-tradefed.jar;%JAR_HOME%\hosttestlib.jar;%JAR_HOME%\ddmlib-prebuilt.jar;%JAR_HOME%\tradefed-prebuilt.jar

java -Xmx512M -cp %JAR_PATH% -DXTS_ROOT=%XTS_ROOT% com.android.xts.tradefed.command.XtsConsole %*