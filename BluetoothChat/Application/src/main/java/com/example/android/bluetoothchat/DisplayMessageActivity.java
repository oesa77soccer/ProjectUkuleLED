package com.example.android.bluetoothchat;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

public class DisplayMessageActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_message);

        // Get the Intent that started this activity and extract the string
        Intent intent = getIntent();
        String message = intent.getStringExtra(UkMain.EXTRA_MESSAGE);

        // Capture the layout's TextView and set the string as its text

        // if there's a problem... it's here
        TextView textView = (TextView) findViewById(R.id.textView);
        //

        textView.setText(message);
    }
}

