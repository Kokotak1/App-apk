package cz.youarefree.pipboy.countdown;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.graphics.drawable.GradientDrawable;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Locale;

/**
 * Tappable companion for Pip-Boy RED.
 * Counts down to the first instant of 1 August 2027 in the Prague time zone.
 * Works entirely offline, including across daylight-saving changes.
 */
public final class CountdownActivity extends Activity {
    private static final ZoneId PRAGUE = ZoneId.of("Europe/Prague");
    private static final Instant DEADLINE =
            LocalDate.of(2027, 8, 1).atStartOfDay(PRAGUE).toInstant();
    private static final int GREEN = Color.rgb(38, 236, 67);
    private static final int MUTED_GREEN = Color.rgb(137, 188, 142);
    private static final int RED = Color.rgb(255, 45, 45);
    private static final int DARK = Color.rgb(3, 12, 7);

    private TextView remainingHours;
    private TextView remainingBreakdown;
    private TextView remainingSeconds;
    private final Handler handler = new Handler(Looper.getMainLooper());

    private final Runnable tick = new Runnable() {
        @Override public void run() {
            renderCountdown();
            handler.postDelayed(this, 1000);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.BLACK);
        getWindow().setNavigationBarColor(Color.BLACK);
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setBackgroundColor(Color.BLACK);
        root.setPadding(dp(24), dp(18), dp(24), dp(18));

        TextView badge = label("VAULT-TEC  •  ODPOČET", 12, MUTED_GREEN, Typeface.BOLD);
        root.addView(badge);

        TextView heading = label("DO 1. 8. 2027", 23, Color.WHITE, Typeface.BOLD);
        root.addView(heading, withTop(9));

        remainingHours = label("—", 53, RED, Typeface.BOLD);
        remainingHours.setIncludeFontPadding(false);
        root.addView(remainingHours, withTop(8));

        TextView unit = label("ZBÝVÁ HODIN", 15, GREEN, Typeface.BOLD);
        root.addView(unit, withTop(1));

        remainingBreakdown = label("—", 14, Color.WHITE, Typeface.NORMAL);
        root.addView(remainingBreakdown, withTop(10));

        remainingSeconds = label("—", 12, MUTED_GREEN, Typeface.NORMAL);
        root.addView(remainingSeconds, withTop(4));

        TextView back = label("‹  ZPĚT NA CIFERNÍK", 12, GREEN, Typeface.BOLD);
        GradientDrawable button = new GradientDrawable();
        button.setColor(DARK);
        button.setCornerRadius(dp(18));
        button.setStroke(dp(1), GREEN);
        back.setBackground(button);
        back.setPadding(dp(11), dp(8), dp(11), dp(8));
        back.setOnClickListener(v -> finish());
        root.addView(back, withTop(14));

        setContentView(root);
    }

    private TextView label(String text, int sp, int color, int weight) {
        TextView view = new TextView(this);
        view.setText(text);
        view.setTextSize(sp);
        view.setTextColor(color);
        view.setTypeface(Typeface.create("sans-serif-condensed", weight));
        view.setGravity(Gravity.CENTER);
        view.setSingleLine(true);
        return view;
    }

    private LinearLayout.LayoutParams withTop(int marginDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        params.topMargin = dp(marginDp);
        return params;
    }

    private int dp(int value) {
        return Math.round(getResources().getDisplayMetrics().density * value);
    }

    private void renderCountdown() {
        Duration duration = Duration.between(Instant.now(), DEADLINE);
        if (duration.isNegative() || duration.isZero()) {
            remainingHours.setText("0");
            remainingBreakdown.setText("CÍL DOSAŽEN");
            remainingSeconds.setText("1. 8. 2027, 00:00");
            return;
        }
        long seconds = duration.getSeconds();
        long hours = seconds / 3600;
        long days = seconds / 86400;
        long minutes = (seconds / 60) % 60;
        long remainder = seconds % 60;
        remainingHours.setText(String.format(Locale.US, "%,d", hours)
                .replace(',', ' '));
        remainingBreakdown.setText(
                String.format(Locale.forLanguageTag("cs-CZ"), "%d dní  •  %02d min", days, minutes));
        remainingSeconds.setText(
                String.format(Locale.US, "a %02d sekund", remainder));
    }

    @Override protected void onResume() {
        super.onResume();
        handler.removeCallbacks(tick);
        handler.post(tick);
    }

    @Override protected void onPause() {
        handler.removeCallbacks(tick);
        super.onPause();
    }
}
