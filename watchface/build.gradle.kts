plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboyred22eco"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboyred21eco"
        minSdk = 33
        targetSdk = 36
        versionCode = 9
        versionName = "2.2"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
