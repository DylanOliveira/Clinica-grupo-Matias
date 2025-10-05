package br.edu.clinica.controller;

import br.edu.clinica.model.Atendimento;
import br.edu.clinica.service.AtendimentoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/atendimentos")
public class AtendimentoController {

    private final AtendimentoService service;

    public AtendimentoController(AtendimentoService service) {
        this.service = service;
    }

    @GetMapping
    public List<Atendimento> listar() {
        return service.listar();
    }

    @PostMapping
    public Atendimento criar(@RequestBody Atendimento a) {
        return service.salvar(a);
    }
}
