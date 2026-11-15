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
        versionCode = 2
        versionName = "1.4"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
