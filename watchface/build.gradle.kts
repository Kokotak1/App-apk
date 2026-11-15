plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred9"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred9"
        minSdk = 33
        targetSdk = 36
        versionCode = 6
        versionName = "1.9"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
