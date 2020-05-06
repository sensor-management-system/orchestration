<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <h1>Welcome to the Sensor System Management tool</h1>
        <p>The purpose of this application is to help scientists and technicans to...</p>
        <p>
          If you don't have an account, you can browse and view all datasets.<br>
          If you're already registered, you can login below
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="2">
        <v-text-field
          label="username"
        />
      </v-col>
      <v-col cols="12" md="2">
        <v-text-field
          label="password"
          type="password"
        />
      </v-col>
      <v-col cols="12" md="2">
        <v-btn color="primary">
          Login
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
