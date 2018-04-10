package com.example.android.bluetoothchat;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;

public class ChordProgression extends AppCompatActivity {
    static String[] chordArray = new String[4];
    TextView textView1;
    TextView textView2;
    TextView textView3;
    TextView textView4;

    //place a method here if the action causes something on this screen
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chord_progression);
        Intent intent = getIntent();

        CustomChord.switch1_checked = false;
        CustomChord.switch2_checked = false;
        CustomChord.switch3_checked = false;
        CustomChord.switch4_checked = false;
        String extra1 = intent.getStringExtra("chord1");
        TextView textView1 = (TextView) findViewById(R.id.textViewFirst);
        String extra2 = intent.getStringExtra("chord2");
        TextView textView2 = (TextView) findViewById(R.id.textViewSecond);
        String extra3 = intent.getStringExtra("chord3");
        TextView textView3 = (TextView) findViewById(R.id.textViewThird);
        String extra4 = intent.getStringExtra("chord4");
        TextView textView4 = (TextView) findViewById(R.id.textViewFourth);

        if (chordArray[0] != extra1 && extra1 != null){
            chordArray[0] = extra1;
        }
        if (chordArray[1] != extra2 && extra2 != null){
            chordArray[1] = extra2;
        }
        if (chordArray[2] != extra3 && extra3 != null){
            chordArray[2] = extra3;
        }
        if (chordArray[3] != extra4 && extra4 != null){
            chordArray[3] = extra4;
        }

        textView1.setText(chordArray[0]);
        textView2.setText(chordArray[1]);
        textView3.setText(chordArray[2]);
        textView4.setText(chordArray[3]);
    }

    public void clearAllChords(View view){
        Intent intent = new Intent();
    }

    public void setCustomChord1(View view) {
        // Do something in response to button
        Intent intent = new Intent(this, CustomChord.class);
        String chordNum = view.getTag().toString();
        intent.putExtra("chordNum", chordNum);
        startActivity(intent);
    }

    public void setCustomChord2(View view) {
        // Do something in response to button
        Intent intent = new Intent(this, CustomChord.class);
        String chordNum = view.getTag().toString();
        intent.putExtra("chordNum", chordNum);
        startActivity(intent);
    }

    public void setCustomChord3(View view) {
        // Do something in response to button
        Intent intent = new Intent(this, CustomChord.class);
        String chordNum = view.getTag().toString();
        intent.putExtra("chordNum", chordNum);
        startActivity(intent);
    }

    public void setCustomChord4(View view) {
        // Do something in response to button
        Intent intent = new Intent(this, CustomChord.class);
        String chordNum = view.getTag().toString();
        intent.putExtra("chordNum", chordNum);
        startActivity(intent);
    }
}
