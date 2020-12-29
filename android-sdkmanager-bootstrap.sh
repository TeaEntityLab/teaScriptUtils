# Credit: caller9@stackoverflow.com
# Ref: https://stackoverflow.com/questions/60440509/android-command-line-tools-sdkmanager-always-shows-warning-could-not-create-se
# export ANDROID_HOME=$PWD/android-sdk-linux
yes | android-sdk-linux/tools/bin/sdkmanager --sdk_root=${ANDROID_HOME} --licenses
android-sdk-linux/tools/bin/sdkmanager --sdk_root=${ANDROID_HOME} "platform-tools" "platforms;android-${ANDROID_COMPILE_SDK}" >/dev/null
