plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred6"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred4"
        minSdk = 33
        targetSdk = 36
        versionCode = 3
        versionName = "1.6"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
