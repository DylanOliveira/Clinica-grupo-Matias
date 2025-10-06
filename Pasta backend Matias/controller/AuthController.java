package com.tdebackend.clinicatde.controller;

import com.tdebackend.clinicatde.model.Usuario;
import com.tdebackend.clinicatde.security.JwtUtility;
import com.tdebackend.clinicatde.service.AuthService;
import com.tdebackend.clinicatde.service.UsuarioService;
import com.tdebackend.clinicatde.util.LoginRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/login")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping
    public ResponseEntity<Map<String, String>> login(@RequestBody LoginRequest body) {
        String usuario = body.getUsuario();
        String senha = body.getSenha();

        String authenticatedUser = authService.authenticate(usuario, senha);
        Map<String, String> response = new HashMap<>();

        if (authenticatedUser != null && !authenticatedUser.isEmpty()){
            String token = JwtUtility.generateToken(usuario, Collections.singletonList(authenticatedUser));


            response.put("token", token);
            return ResponseEntity.ok(response);
        }

        response.put("msg", "Credenciais inválidas");
        return ResponseEntity.status(401).body(response);
    }
}
