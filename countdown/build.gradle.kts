plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboy.countdown"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboy.countdown7"
        minSdk = 33
        targetSdk = 36
        versionCode = 2
        versionName = "1.1"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
