plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred3"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred3"
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "1.3"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
