package com.example.android.bluetoothchat;

/**
 * Created by Logan on 4/10/2018.
 */

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;

class Chord
{
    public String chord;
    public boolean minor, sus, aug, sev;

    public Chord() {
        chord = null;
        minor = sus = aug = sev = false;
    }
}

public class CustomChord extends AppCompatActivity {
    static Chord[] chordArray = {new Chord(), new Chord(), new Chord(), new Chord()};
    String cNum = "chord0";
    int chordID;
    String savedExtra = "";
    Switch switch1_view;
    Switch switch2_view;
    Switch switch3_view;
    Switch switch4_view;

    static boolean switch1_checked;
    static boolean switch2_checked;
    static boolean switch3_checked;
    static boolean switch4_checked;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_custom_chord);
        Intent intent = getIntent();
        Button btn = (Button) findViewById(R.id.OKbutton);

        cNum = intent.getStringExtra("chordNum");
        if (cNum.compareTo("chord1") == 0) {
            chordID = 0;
        }
        else if (cNum.compareTo("chord2") == 0) {
            chordID = 1;
        }
        else if (cNum.compareTo("chord3") == 0) {
            chordID = 2;
        }
        else if (cNum.compareTo("chord4") == 0) {
            chordID = 3;
        }

        savedExtra = intent.getStringExtra("note");
        if (savedExtra == null) {
            if(chordArray[chordID].chord != null) {
                btn.setEnabled(true);
                savedExtra = chordArray[chordID].chord;
            } else btn.setEnabled(false); }
        else {
            btn.setEnabled(true); }


        TextView myText = (TextView) findViewById(R.id.chordNameID);
        myText.setText(savedExtra);

        // initialize screen to use stored chord values
        switch1_checked = chordArray[chordID].minor;
        switch2_checked = chordArray[chordID].sus;
        switch3_checked = chordArray[chordID].aug;
        switch4_checked = chordArray[chordID].sev;

        // set up listener for switches
        switch1_view = (Switch) findViewById(R.id.switch1);
        switch1_view.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch1_checked = isChecked;
                chordArray[chordID].minor = switch1_checked;
            }
        });
        switch2_view = (Switch) findViewById(R.id.switch2);
        switch2_view.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch2_checked = isChecked;
                chordArray[chordID].sus = switch2_checked;
            }
        });
        switch3_view = (Switch) findViewById(R.id.switch3);
        switch3_view.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch3_checked = isChecked;
                chordArray[chordID].aug = switch3_checked;
            }
        });
        switch4_view = (Switch) findViewById(R.id.switch4);
        switch4_view.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch4_checked = isChecked;
                chordArray[chordID].sev = switch4_checked;
            }
        });
        // check to see if the switches are supposed to start on

        switch1_view.setChecked(switch1_checked);
        switch2_view.setChecked(switch2_checked);
        switch3_view.setChecked(switch3_checked);
        switch4_view.setChecked(switch4_checked);
    }

    public void setChordNote(View view) {
        // Do something in response to button
        Intent intent = new Intent(this, ChordNoteList.class);
        intent.putExtra("chordNum", cNum);
        startActivity(intent);
    }
    public void placeChordNameInChordProgression(View view) {
        // Do something in response to button
        Intent intent = new Intent(this, ChordProgression.class);
        intent.putExtra("chordNum", cNum);


        //if (findViewById(R.id.switch1))
        /*if (switch1_checked) savedExtra += "m";
        if (switch2_checked) savedExtra += " sus";
        if (switch3_checked) savedExtra += " aug";
        if (switch4_checked) savedExtra += "7";*/
        //savedExtra += "X";

        chordArray[chordID].chord = savedExtra;
        if (chordArray[chordID].minor) savedExtra += "m";
        if (chordArray[chordID].sus) savedExtra += " sus";
        if (chordArray[chordID].aug) savedExtra += " aug";
        if (chordArray[chordID].sev) savedExtra += "7";

        if(cNum.compareTo("chord1") == 0) {
            intent.putExtra("chord1", savedExtra);
        }
        if(cNum.compareTo("chord2") == 0) {
            intent.putExtra("chord2", savedExtra);
        }
        if(cNum.compareTo("chord3") == 0) {
            intent.putExtra("chord3", savedExtra);
        }
        if(cNum.compareTo("chord4") == 0) {
            intent.putExtra("chord4", savedExtra);
        }
        startActivity(intent);
    }
}
