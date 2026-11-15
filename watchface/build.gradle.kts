plugins {
    id("com.android.application")
}
android {
    namespace = "cz.youarefree.pipboy"
    compileSdk = 36
    defaultConfig {
        applicationId = "cz.youarefree.pipboy"
        minSdk = 33
        targetSdk = 36
        versionCode = 2
        versionName = "1.1"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
}
