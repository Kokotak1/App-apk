plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboy.countdown"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboy.countdown"
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
