plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred7"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred7"
        minSdk = 33
        targetSdk = 36
        versionCode = 4
        versionName = "1.7"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
