plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred24eco"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred24eco"
        minSdk = 33
        targetSdk = 36
        versionCode = 11
        versionName = "2.4"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
