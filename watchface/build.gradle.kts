plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred21eco"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred21eco"
        minSdk = 33
        targetSdk = 36
        versionCode = 8
        versionName = "2.1"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
